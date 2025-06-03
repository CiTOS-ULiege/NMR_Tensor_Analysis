import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import os

def plot_crude(chemical_shifts, rmn_data, times,base_path):
    n = times.shape[0]
    n_normalized = np.linspace(0, 1, n)
    colors = plt.cm.jet(n_normalized)
    norm = Normalize(vmin=times[0], vmax=times[-1])
    fig = plt.figure(figsize=(24, 16), dpi=300)
    main_ax = fig.add_axes([0.15, 0.2, 0.75, 0.7])
    for i in range(n):
        main_ax.plot(chemical_shifts, rmn_data[i,:], linewidth=0.75, color=colors[i])
    main_ax.set_ylabel('Intensities (a.u.)', fontsize=8, labelpad=5)
    main_ax.set_xlabel('Shifts (ppm)', fontsize=8, labelpad=10)
    x_min, x_max = chemical_shifts.min(), chemical_shifts.max()
    x_ticks = np.arange(np.floor(x_min * 2) / 2, np.ceil(x_max * 2) / 2 + 0.5, 0.5)
    main_ax.set_xticks(x_ticks)
    main_ax.set_xlim(x_min, x_max)
    main_ax.tick_params(axis='both', which='major', labelsize=8, pad=3)
    main_ax.xaxis.set_label_coords(0.5, -0.14)
    main_ax.set_title('NMR Spectra Over Time', fontsize=10, pad=10)
    cbar_ax = fig.add_axes([0.91, 0.2, 0.02, 0.7])
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.ax.set_title('Time (min)', fontsize=8, pad=10)
    cbar.ax.tick_params(labelsize=8)
    #plt.tight_layout()
    plt.savefig(os.path.join(base_path, 'Figure_NMR.png'), dpi=300, bbox_inches='tight')
    plt.show(block=False)
    

def subplot1(mean_bic_by_rank, mean_aic_by_rank, errors, explained_variances, errors_by_rank,base_path):
    
    ranks = list(range(1, 12 + 1))
    fig = plt.figure(figsize=(15,10))
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.25, 
                    hspace=0.25)
    
    ax1 = fig.add_subplot(2,3,1)
    ax1.bar(mean_bic_by_rank.keys(), mean_bic_by_rank.values(), color='skyblue')
    ax1.set_title('Mean BIC for Each Rank')
    ax1.set_xlabel('Rank')
    ax1.set_ylabel('BIC')
    ax1.set_xticks(list(mean_bic_by_rank.keys()))

    ax2 = fig.add_subplot(2,3,2)
    ax2.bar(mean_aic_by_rank.keys(), mean_aic_by_rank.values(), color='salmon')
    ax2.set_title('Mean AIC for Each Rank')
    ax2.set_xlabel('Rank')
    ax2.set_ylabel('AIC')
    ax2.set_xticks(list(mean_aic_by_rank.keys()))
    

    ax3 = fig.add_subplot(2,3,3)
    ax3.plot(ranks, errors, '-o', color='b', label="Erreur de reconstruction")
    ax3.set_xlabel("Rank")
    ax3.set_ylabel("Reconstruction error", color='b')
    ax3.tick_params(axis='y', labelcolor='b')
    ax3.set_title("Reconstruction error and explained variance")
    ax4 = ax3.twinx()
    ax4.plot(ranks, explained_variances, '-o', color='r', label="Explained variance")  
    ax4.set_ylabel("Explained variance", color='r')
    ax4.tick_params(axis='y', labelcolor='r')



    ax5 = fig.add_subplot(2,3,4)
    avg_changes = {}
    ranks = list(errors_by_rank.keys())
    
    for rank, errors in errors_by_rank.items():
        train_errors = [error[0] for error in errors]
        ax5.plot(range(1, len(train_errors) + 1), train_errors, marker='o', label=f'Rank {rank}')
        
        if len(train_errors) > 1:
            percent_change = np.diff(train_errors) / train_errors[:-1] * 100
            avg_change = np.mean(percent_change)
            avg_changes[rank] = avg_change
    
    ax5.set_title('Learning Curve (Training Error Only)')
    ax5.set_xlabel('Test Point Index')
    ax5.set_ylabel('Reconstruction Error')
    ax5.legend(loc='best', ncol=3)

    ax6 = fig.add_subplot(2,3,5)
    ranks = list(errors_by_rank.keys())
    error_data = [list(zip(*errors))[0] for errors in errors_by_rank.values()]
    
    # Boîte à moustaches (Boxplot)
    ax6.boxplot(error_data, labels=ranks)
    ax6.set_title('Error Distribution Across Ranks')
    ax6.set_xlabel('Rank')
    ax6.set_ylabel('Reconstruction Error')
    
    ax7 = fig.add_subplot(2,3,6)
    ranks = list(errors_by_rank.keys())
    avg_train_errors = [np.mean([error[0] for error in errors]) for errors in errors_by_rank.values()]
    
    ax7.plot(ranks, avg_train_errors, marker='o', linestyle='-', color='blue', label='Average Training Error')
    ax7.set_ylabel('Average Training Error', color='b')
    ax7.tick_params(axis='y', labelcolor='b')
    
    ax8 = ax7.twinx()
    
    if len(ranks) > 1:
        derivatives = np.diff(avg_train_errors) / np.diff(ranks)
        ax8.plot(ranks[1:], derivatives, marker='o', linestyle='-', color='red', label='Derivative of Error')
    
    ax8.set_ylabel('Average Training Error derivative', color='red')
    ax8.tick_params(axis='y', labelcolor='red')
    
    ax7.set_title('Model Complexity vs Training Error and Derivative')
    ax7.set_xlabel('Rank')
    
    plt.savefig(os.path.join(base_path, 'subplot1.png'), dpi=300, bbox_inches='tight')
    
    plt.show(block=False)
    
    

def subplot2(chemical_shifts, rmn_data, times, results, ranks_to_analyze, average_factors,base_path):
    fig = plt.figure(figsize=(15, 10))
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.25, hspace=0.25)
    
    
    # Création de ax1 avec plot_crude
    ax1 = fig.add_subplot(2, 3, 1)
    n = times.shape[0]
    n_normalized = np.linspace(0, 1, n)
    colors = plt.cm.jet(n_normalized)
    norm = Normalize(vmin=times[0], vmax=times[-1])
    
    for i in range(n):
        ax1.plot(chemical_shifts, rmn_data[i,:], linewidth=0.75, color=colors[i])

    ax1.set_ylabel('Intensities (a.u.)', fontsize=8, labelpad=5)
    ax1.set_xlabel('Shifts (ppm)', fontsize=8, labelpad=10)
    
    x_min, x_max = chemical_shifts.min(), chemical_shifts.max()
    x_ticks = np.arange(np.floor(x_min * 2) / 2, np.ceil(x_max * 2) / 2 + 0.5, 0.5)
    ax1.set_xticks(x_ticks)
    ax1.set_xlim(x_min, x_max)
    
    ax1.tick_params(axis='both', which='major', labelsize=8, pad=3)
    ax1.set_title('NMR Spectra Over Time', fontsize=10, pad=10)

    # Colorbar pour ax1
    #cbar_ax = fig.add_axes([0.3, 0.08, 0.02, 0.2])  # Ajusté pour s'adapter à la mise en page
    #sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
    #sm.set_array([])
    #cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
    #cbar.set_label('Time (min)', fontsize=8, labelpad=5)
    #cbar.ax.tick_params(labelsize=8)
    
    ax2 = fig.add_subplot(2, 3, 2)
    ranks = list(results.keys())
    ax2.set_title("Error distribution by rank")
    error_data = [[rep['error'] for rep in results[rank]] for rank in ranks]
    ax2.boxplot(error_data, labels=ranks)
    ax2.set_xlabel("Rank")
    ax2.set_ylabel("Reconstruction error")
    
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.set_title("Variance distribution by rank")
    variance_data = [[rep['explained_variance'] for rep in results[rank]] for rank in ranks]
    ax3.boxplot(variance_data, labels=ranks)
    ax3.set_xlabel("Rank")
    ax3.set_ylabel("Explained variance")
    
    
    concentrations_dict = {}
    normalized_concentrations_dict = {}
    
    for i, rank in enumerate(ranks_to_analyze):
        ax = fig.add_subplot(2, 3, 4 + i)
        
        concentrations = average_factors[rank][0]
        
        concentrations_array = np.array(concentrations)
        concentrations_dict[f"rank_{rank}"] = concentrations_array
        
        array_min = np.min(concentrations_array)
        array_max = np.max(concentrations_array)
        normalized_concentrations = (concentrations_array - array_min) / (array_max - array_min)
        
        normalized_concentrations_dict[f"rank_{rank}"] = normalized_concentrations
        
        # Utiliser les concentrations normalisées pour le tracé
        ax.plot(times, normalized_concentrations, label="Normalized")
        ax.set_title(f"Normalized concentrations (Rank {rank})")
        ax.set_xlabel("Time (min)")
        ax.set_ylabel("Normalized concentrations")
        
        
    plt.savefig(os.path.join(base_path, 'subplot2.png'), dpi=300, bbox_inches='tight')
    plt.show(block=False)
    
    
       
    return concentrations_dict, normalized_concentrations_dict