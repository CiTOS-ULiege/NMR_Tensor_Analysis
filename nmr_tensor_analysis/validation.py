"""
Tensor Decomposition Model Evaluation with Temporal Cross-Validation

This module implements evaluation metrics (BIC/AIC) and temporal cross-validation 
for comparing tensor decomposition models of different ranks.
"""
import numpy as np
from .decomposition import unfold_tensor

def calculate_bic(n, k, residual_sum_of_squares):
    bic = n * np.log(residual_sum_of_squares / n) + k * np.log(n)
    return bic

def calculate_aic(n, k, residual_sum_of_squares):
    aic = n * np.log(residual_sum_of_squares / n) + 2 * k
    return aic

def temporal_cross_val_2d(unfolded_tensors, X, initial_train_size=5):
    """
       Perform temporal cross-validation on tensor decomposition models
    
    Args:
        unfolded_tensors (dict): Dictionary {rank: unfolded_tensor} 
            containing decomposed tensors
        X (np.ndarray): Original 3D tensor (I x J x K)
        initial_train_size (int): Initial training window size
    
    """
    I_original, J, K = X.shape
    n_splits = X.shape[0] - initial_train_size
    errors_by_rank = {rank: [] for rank in unfolded_tensors.keys()}
    residuals_by_rank = {rank: [] for rank in unfolded_tensors.keys()}
    bic_by_rank = {rank: [] for rank in unfolded_tensors.keys()}
    aic_by_rank = {rank: [] for rank in unfolded_tensors.keys()}
    X = unfold_tensor(X, mode=0)
    for fold in range(n_splits):
        train_end = initial_train_size + fold
        I_train = train_end
        test_index = train_end
        train_indices = list(range(train_end))
        X_real_train = X[:train_end]
        X_real_test = X[test_index:test_index+1]
        for rank, X_unfolded in unfolded_tensors.items():
            X_approx_train = X_unfolded[:train_end]
            X_approx_test = X_unfolded[test_index:test_index+1]
            error_train = np.linalg.norm(X_real_train - X_approx_train, 'fro')
            error_test = np.linalg.norm(X_real_test - X_approx_test, 'fro')
            errors_by_rank[rank].append((error_train, error_test))
            residuals = X_real_train - X_approx_train
            residuals_by_rank[rank].append(residuals[-1])
            n = X_real_train.size
            core_params = rank ** 3
            factor_params = I_train*rank + J*rank + K*rank
            k = core_params + factor_params
            residual_sum_of_squares = np.sum(residuals**2)
            bic = calculate_bic(n, k, residual_sum_of_squares)
            aic = calculate_aic(n, k, residual_sum_of_squares)
            bic_by_rank[rank].append(bic)
            aic_by_rank[rank].append(aic)
    mean_residuals_by_rank = {rank: np.mean(residuals, axis=0) for rank, residuals in residuals_by_rank.items()}
    mean_bic_by_rank = {rank: np.mean(bic_values) for rank, bic_values in bic_by_rank.items()}
    mean_aic_by_rank = {rank: np.mean(aic_values) for rank, aic_values in aic_by_rank.items()}
    return errors_by_rank, mean_residuals_by_rank, mean_bic_by_rank, mean_aic_by_rank
