**Tools for Computer-Aided Kinetic Modeling (Part 1)**
---
**Research context**
The tools described in this repository were developed as part of the research on the mechanistic study of dynamic covalent exchanges of orthoesters with diols.

**Access to the Repository**
First, clone the repository to your local machine:
```python
git clone https://github.com/CiTOS-ULiege/nmr_tensor_analysis.git
```
Install the requirements:
```python
pip install -r requirements.txt
```
Finally, run the code: 
```python
python main.py
```
**Computer-Aided Kinetic Network Modeling of Orthoester Metathesis**
*Claire Muzyka,<sup>a</sup> Tom Perreira Rodrigues,<sup>a</sup> Diana V. Silva-Brenes,<sup>a,b</sup> and Jean-Christophe M. Monbaliu<sup>\*,a,c</sup>.* 

Center for Integrated Technology and Organic Synthesis (CiTOS), MolSys Research Unit, University of Liège, Allée du Six Août 13, B-4000 Liège (Sart Tilman), Belgium 
E-mail: <jc.monbaliu@uliege.be> | <www.citos.uliege.be>
b. FloW4all Flow Technology Resource Center, University of Liège, B-4000 Liège (Sart-Tilman), Belgium
c. WEL Research Institute, Avenue Pasteur, 6, 1300 Wavre, Belgium.

### Usage Instructions:

This Python script provides a complete workflow for analyzing raw <sup>1</sup>H-NMR kinetic data by applying a non-negative Tucker tensor decomposition. The main steps of the code are as follows:

**a) Data Loading:** The user is prompted to select an Excel file through a dialog box. The required file format is: the first row contains time points, the first column contains chemical shifts, and the top-left cell (A1) must remain empty (example in the data folder). Each subsequent column represents a spectrum acquired at a given time. The data is imported automatically and prepared for further processing.
```python
import tkinter as tk
from nmr_tensor_analysis.io_utils import ask_best_rank, select_file, select_folder_to_save
from nmr_tensor_analysis.preprocessing import prepare_rmn_data, split_data, preprocess_rmn_data
from nmr_tensor_analysis.decomposition import tucker_analysis, tucker_sensitivity_analysis
from nmr_tensor_analysis.validation import temporal_cross_val_2d 
from nmr_tensor_analysis.plotting import plot_crude, subplot1, subplot2

# Initialize the Tkinter window (but keep it hidden)
root = tk.Tk()
root.withdraw()

# 1. Select the data file
data = select_file()  # Opens a dialog box to select an Excel file

# 2. Select the folder to save results
base_path = select_folder_to_save()  # Opens a dialog box to select a folder
```
**b) Signal Processing:** After loading, the data undergoes automated signal treatment, including a 2D median filter and a Savitzky-Golay filter. This dual filtering improves the signal-to-noise ratio while preserving crucial spectral features such as peak width, height, and coupling patterns. The processed data are then visualized for inspection.
```python 
# 3. Preprocess the data
times, chemical_shifts, rmn_data = prepare_rmn_data(data)
rmn_data = preprocess_rmn_data(rmn_data)  # Apply 2D median filter and Savitzky-Golay
# 4. Visualize the preprocessed data
plot_crude(chemical_shifts, rmn_data, times)
```
![enter image description here](https://lh3.googleusercontent.com/d/1zdm9EYfw60zVS7h-6r_nmGYPpgXqUV8M)

**c) Tensor Construction:** The 2D NMR data matrix is transformed into a 3D tensor by sequentially grouping chemical shifts into five matrices of equal size. This procedure introduces a third dimension, enabling tensor decomposition. For example, chemical shifts at 1.00, 1.01, 1.02, 1.03, and 1.04 ppm are each assigned to separate matrices.
```python 
# 5. Transform into 3D tensor
X = split_data(rmn_data, 5)  # Transform the 2D matrix into a 3D tensor
```
**d) Non-Negative Tucker Decomposition:** A non-negative Tucker decomposition is performed on the treated data to ensure all values remain physically meaningful (positive). This approach is also applicable to other spectroscopic data such as Raman or IR. The script explores decomposition ranks from 1 to 12, corresponding to the potential number of species in the kinetic dataset. Prior to Tucker decomposition, a non-negative matrix factorization (NMF) is applied for initialization, using NNDSVDAR (non-negative double singular value decomposition with random alternation), a coordinate descent solver, regularization parameters (αH and αW) set to 0.1, an L1 ratio of 0.01, and Frobenius norm as the cost function. The resulting W and H matrices initialize the first two factors of the Tucker model, while the third factor and the tensor core are randomly initialized. For each rank, a reconstructed tensor is computed. Quantitative metrics are calculated to assess reconstruction accuracy, including the relative reconstruction error and the explained variance, both based on the Frobenius norm.
```python 
# 6. Tucker decomposition analysis
max_rank = 12  # Test ranks from 1 to 12
errors, results, tensors_by_rank, explained_variances, unfolded_tensors = tucker_analysis(
    X, max_rank, tol=1e-4, unfold_mode=0)
```
**e) Cross-Validation:** A temporal cross-validation is performed on the unfolded tensors at each rank. Tensor unfolding transforms the 3D tensor into a 2D matrix, matching the original data format. For each rank, the unfolded matrices are evaluated sequentially over time. Training begins with the first five time points, and the model is tested on the next (sixth) point. At each iteration, the Bayesian Information Criterion (BIC) and Akaike Information Criterion (AIC) are computed. This process repeats for all subsequent time points, and mean BIC/AIC values are calculated for each rank to guide model selection.
```python 
# 7. Temporal cross-validation
errors_CV, mean_residuals, mean_bic, mean_aic = temporal_cross_val_2d(
    unfolded_tensors, X, initial_train_size=5)
```
**f) Operator Decision:** All metrics (reconstruction error, explained variance, BIC, AIC, learning curves, and their derivatives) are displayed in graphical outputs. Based on these, the user is prompted to select the optimal rank (number of compounds) using a dialog box.
```python 
# 8. Visualize the analysis results
subplot1(mean_bic, mean_aic, errors, explained_variances, errors_CV, base_path)

# 9. Ask the user to choose the optimal rank
best_rank = ask_best_rank()
```
![n here](https://lh3.googleusercontent.com/d/1z6VsEoGmMvWYeMp7SMPrKi3glTb2662h)

**g) Sensitivity Analysis:** Once the optimal rank is chosen, the script performs 10 repetitions of the non-negative Tucker decomposition with distinct NMF initializations for the best rank, as well as for the neighboring ranks (best rank -1 and best rank +1). For each repetition, the relative error and explained variance are computed. A second set of graphical outputs illustrates the variability of these metrics across runs, providing insight into the robustness of the decomposition and the stability of concentration profiles.
```python 
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
```
![enter image description here](https://lh3.googleusercontent.com/d/1jJXpFY0AgJGW0vo1rdPS7SlPcJiPCxqC)

**Scope and Limitations:** This tool offers preliminary statistical indicators to support the analysis of complex NMR kinetic data. It is designed to estimate the minimal number of compounds in a mixture. However, it does not replace comprehensive structural characterization. The results should be interpreted as working hypotheses to be validated experimentally. The tool is less effective for trace species or highly overlapping signals.

**Funding**
This research program was funded by the University of Liege, the French Community of Belgium (Concerted Research Action CO2FLUIDICS 21/25-04). Computational resources were provided by the “Consortium des Équipements de Calcul Intensif” (CÉCI), funded by the “Fonds de la Recherche Scientifique de Belgique” (F.R.S.-FNRS) under Grant No. 2.5020.11a. 

**Acknowledgments**
This research program was funded by the University of Liege, the French Community of Belgium (Concerted Research Action CO2FLUIDICS 21/25-04). Dr. Christophe Detrembleur (Concerted Research Action CO2FLUIDICS 21/25-04, PI) and Dr. Bruno Grignard (Concerted Research Action CO2FLUIDICS 21/25-04, Collaborator) are acknowledged for their support. The authors acknowledge the “Fonds de la Recherche Scientifique (F.R.S.-FNRS) for funding. Computational resources were provided by the “Consortium des Équipements de Calcul Intensif” (CÉCI), funded by the “Fonds de la Recherche Scientifique de Belgique” (F.R.S.-FNRS) under Grant No. 2.5020.11a. The manuscript was written through contributions of all authors. All authors have given approval to the final version of the manuscript.

**Attributions**
The code in this repository is licensed under the MIT License. You are free to use, modify, and distribute the code under the terms of this license.
```
