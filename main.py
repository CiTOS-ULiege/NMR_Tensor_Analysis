<<<<<<< HEAD
import tkinter as tk
from nmr_tensor_analysis.io_utils import ask_best_rank, select_file, select_folder_to_save
from nmr_tensor_analysis.preprocessing import prepare_rmn_data, split_data, preprocess_rmn_data
from nmr_tensor_analysis.decomposition import tucker_analysis, tucker_sensitivity_analysis
from nmr_tensor_analysis.validation import temporal_cross_val_2d 
from nmr_tensor_analysis.plotting import plot_crude, subplot1, subplot2

def main():
    # Initialize the Tkinter window (but keep it hidden)
    root = tk.Tk()
    root.withdraw()

    # 1. Select the data file
    data = select_file()
    if data is None:
        print("No file selected. Exiting.")
        return

    # 2. Select the folder to save results
    base_path = select_folder_to_save()
    if base_path is None:
        print("No folder selected. Exiting.")
        return

    # 3. Preprocess the data
    times, chemical_shifts, rmn_data = prepare_rmn_data(data)
    rmn_data = preprocess_rmn_data(rmn_data)

    # 4. Transform into 3D tensor
    X = split_data(rmn_data, 5)

    # 5. Visualize the preprocessed data
    plot_crude(chemical_shifts, rmn_data, times, base_path)

    # 6. Tucker decomposition analysis
    max_rank = 12
    errors, results, tensors_by_rank, explained_variances, unfolded_tensors = tucker_analysis(
        X, max_rank, tol=1e-4, unfold_mode=0
    )

    # 7. Temporal cross-validation
    errors_CV, mean_residuals, mean_bic, mean_aic = temporal_cross_val_2d(
        unfolded_tensors, X, initial_train_size=5
    )

    # 8. Visualize the analysis results
    subplot1(mean_bic, mean_aic, errors, explained_variances, errors_CV, base_path)

    # 9. Ask the user to choose the optimal rank
    best_rank = ask_best_rank()

    # 10. Sensitivity analysis for the chosen rank
    n_repetitions = 10
    results_sensitivity, ranks_to_analyze, average_tensors, average_factors = tucker_sensitivity_analysis(
        X, best_rank, tol=1e-4, n_repetitions=n_repetitions
    )

    # 11. Visualize concentration profiles
    concentrations_dict, normalized_concentrations_dict = subplot2(
        chemical_shifts, rmn_data, times, results_sensitivity, ranks_to_analyze, average_factors, base_path
    )

    print(f"Analysis complete. Results saved to {base_path}")

if __name__ == "__main__":
    main()
=======
import tkinter as tk
from nmr_tensor_analysis.io_utils import ask_best_rank, select_file, select_folder_to_save
from nmr_tensor_analysis.preprocessing import prepare_rmn_data, split_data, preprocess_rmn_data
from nmr_tensor_analysis.decomposition import tucker_analysis, tucker_sensitivity_analysis
from nmr_tensor_analysis.validation import temporal_cross_val_2d 
from nmr_tensor_analysis.plotting import plot_crude, subplot1, subplot2

def main():
    # Initialize the Tkinter window (but keep it hidden)
    root = tk.Tk()
    root.withdraw()

    # 1. Select the data file
    data = select_file()
    if data is None:
        print("No file selected. Exiting.")
        return

    # 2. Select the folder to save results
    base_path = select_folder_to_save()
    if base_path is None:
        print("No folder selected. Exiting.")
        return

    # 3. Preprocess the data
    times, chemical_shifts, rmn_data = prepare_rmn_data(data)
    rmn_data = preprocess_rmn_data(rmn_data)

    # 4. Transform into 3D tensor
    X = split_data(rmn_data, 5)

    # 5. Visualize the preprocessed data
    plot_crude(chemical_shifts, rmn_data, times, base_path)

    # 6. Tucker decomposition analysis
    max_rank = 12
    errors, results, tensors_by_rank, explained_variances, unfolded_tensors = tucker_analysis(
        X, max_rank, tol=1e-4, unfold_mode=0
    )

    # 7. Temporal cross-validation
    errors_CV, mean_residuals, mean_bic, mean_aic = temporal_cross_val_2d(
        unfolded_tensors, X, initial_train_size=5
    )

    # 8. Visualize the analysis results
    subplot1(mean_bic, mean_aic, errors, explained_variances, errors_CV, base_path)

    # 9. Ask the user to choose the optimal rank
    best_rank = ask_best_rank()

    # 10. Sensitivity analysis for the chosen rank
    n_repetitions = 10
    results_sensitivity, ranks_to_analyze, average_tensors, average_factors = tucker_sensitivity_analysis(
        X, best_rank, tol=1e-4, n_repetitions=n_repetitions
    )

    # 11. Visualize concentration profiles
    concentrations_dict, normalized_concentrations_dict = subplot2(
        chemical_shifts, rmn_data, times, results_sensitivity, ranks_to_analyze, average_factors, base_path
    )

    print(f"Analysis complete. Results saved to {base_path}")

if __name__ == "__main__":
    main()
>>>>>>> 3ba84e62b0f35f5867a08fc7304572a01fd8909d
