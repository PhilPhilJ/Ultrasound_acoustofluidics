import numpy as np

def moving_average(arr, window_size):
    """Calculates the moving average of an array with a given window size"""
    pad_width = window_size // 2  # Pad on both sides
    padded_arr = np.pad(arr, pad_width, mode='edge')
    moving_averages = np.convolve(padded_arr, np.ones(window_size) / window_size, 'valid')
    return moving_averages
