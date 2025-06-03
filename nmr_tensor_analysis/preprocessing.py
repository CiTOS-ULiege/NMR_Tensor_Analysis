import matplotlib
matplotlib.use('Qt5Agg')  
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
from scipy import signal
from scipy.signal import savgol_filter


def prepare_rmn_data(data):
    times = data.iloc[0, 1:]
    chemical_shifts = data.iloc[1:, 0]
    rmn_data = data.iloc[1:, 1:]
    times = np.array(times)
    chemical_shifts = np.array(chemical_shifts)
    rmn_data = np.array(rmn_data).T
    return times, chemical_shifts, rmn_data

def split_data(data, n_samples):
    num_columns = data.shape[1]
    max_columns_multiple = (num_columns // n_samples) * n_samples
    data_adjusted = data[:, :max_columns_multiple]
    subsets = []
    for offset in range(n_samples):
        subset = data_adjusted[:, offset::n_samples]
        subsets.append(subset)
    tensor_3d = np.stack(subsets, axis=2)
    return tensor_3d

def preprocess_rmn_data(rmn_data):
    # Median filter
    rmn_data = signal.medfilt2d(rmn_data, kernel_size=3)
    # Savitzky-Golay filter
    window_length = 31
    polyorder = 7
    for i in range(rmn_data.shape[1]):
        data_length = rmn_data.shape[0]
        if window_length > data_length:
            window_length = data_length - (data_length % 2 == 0)
        rmn_data[:, i] = savgol_filter(rmn_data[:, i], window_length=window_length, polyorder=polyorder)
    rmn_data[rmn_data < 0] = 0
    return rmn_data
