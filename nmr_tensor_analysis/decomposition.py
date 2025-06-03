import numpy as np
from sklearn.decomposition import NMF
import tensorly as tl
from tensorly.decomposition import non_negative_tucker
np.random.seed(42)

def frobenius_norm(tensor):
    return np.sqrt(np.sum(tensor**2))

def tucker_analysis(X, max_rank, tol, unfold_mode=0):
    """
    Perform Tucker decomposition analysis across different ranks
    Args:
        X: Input tensor
        max_rank: Maximum rank to investigate
        tol: Tolerance for convergence
        unfold_mode: Matricization mode for tensor unfolding
    Returns analysis metrics and decomposition results
    """
    errors = []
    results = {}
    tensors_by_rank = {}
    explained_variances = []
    unfolded_tensors = {}
    for rank in range(1, max_rank + 1):
        print(f"\nCalculation for the rank {rank} :")
        nmf = NMF(n_components=rank, init='nndsvdar', solver='cd', max_iter=20000, alpha_W=0.1, alpha_H=0.1, l1_ratio=0.001, beta_loss='frobenius')
        W = nmf.fit_transform(X[:, :, 0])
        H = nmf.components_
        factor_mode1 = tl.tensor(W)
        factor_mode2 = tl.tensor(H.T)
        factor_mode3 = tl.tensor(np.random.random((X.shape[2], rank)))
        factors = [factor_mode1, factor_mode2, factor_mode3]
        init_cp_tensor = (np.random.random([rank] * X.ndim), factors)
        tucker_tensor = non_negative_tucker(X, rank=[rank] * X.ndim, init=init_cp_tensor, tol=tol)
        core, factors = tucker_tensor
        X_approx = tl.tucker_to_tensor((core, factors))
        X_approx_unfolded = tl.unfold(X_approx, unfold_mode)
        val_error = frobenius_norm(X - X_approx) / frobenius_norm(X)
        errors.append(val_error)
        explained_variance = 1 - (frobenius_norm(X - X_approx) ** 2) / (tl.norm(X) ** 2)
        explained_variances.append(explained_variance)
        results[rank] = {
            'X_approx': X_approx,
            'core': core,
            'factors': factors,
            'val_error': val_error,
            'explained_variance': explained_variance
        }
        tensors_by_rank[rank] = (core, factors)
        unfolded_tensors[rank] = X_approx_unfolded
    return errors, results, tensors_by_rank, explained_variances, unfolded_tensors

def tucker_sensitivity_analysis(X, best_rank, tol, n_repetitions=10, max_iter=20000):
    """
    Analyze decomposition stability through multiple initializations
    Args:
        best_rank: Central rank for sensitivity analysis
        n_repetitions: Number of random initializations to test
    Returns stability metrics and averaged components
    """
    ranks_to_analyze = [max(1, best_rank - 1), best_rank, best_rank + 1]
    results_sensitivity = {rank: [] for rank in ranks_to_analyze}
    average_tensors = {}
    average_factors = {}
    for rank in ranks_to_analyze:
        print(f"\nAnalysis for the rank {rank}")
        tensors_for_average = []
        factors_for_average = [[] for _ in range(X.ndim)]
        for rep in range(n_repetitions):
            print(f"Repetition {rep + 1}/{n_repetitions}")
            random_seed = rep + 1
            nmf = NMF(n_components=rank, init='nndsvdar', solver='cd', alpha_W=0.1, alpha_H=0.1, l1_ratio=0.001, max_iter=20000, random_state=random_seed, beta_loss='frobenius')
            W = nmf.fit_transform(X[:, :, 0])
            H = nmf.components_
            factor_mode1 = tl.tensor(W)
            factor_mode2 = tl.tensor(H.T)
            factor_mode3 = tl.tensor(np.random.random((X.shape[2], rank)))
            factors = [factor_mode1, factor_mode2, factor_mode3]
            init_cp_tensor = (np.random.random([rank] * X.ndim), factors)
            tucker_tensor = non_negative_tucker(X, rank=[rank] * X.ndim, init=init_cp_tensor, tol=tol)
            core, factors = tucker_tensor
            X_approx = tl.tucker_to_tensor((core, factors))
            tensors_for_average.append(X_approx)
            for i, factor in enumerate(factors):
                factors_for_average[i].append(factor)
            val_error = tl.norm(X - X_approx) / tl.norm(X)
            explained_variance = 1 - (tl.norm(X - X_approx) ** 2) / (tl.norm(X) ** 2)
            results_sensitivity[rank].append({
                'error': val_error,
                'explained_variance': explained_variance,
                'factors': factors,
                'core': core
            })
        average_tensor = np.mean(tensors_for_average, axis=0)
        average_tensors[rank] = average_tensor
        avg_factors = [np.mean(factor_list, axis=0) for factor_list in factors_for_average]
        average_factors[rank] = avg_factors
    return results_sensitivity, ranks_to_analyze, average_tensors, average_factors

def unfold_tensor(X, mode=0):
    return tl.unfold(X, mode)
