import cv2, os, sys
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

sys.path.append('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Ultrasound_acoustofluidics/')

# Define functions
def func(t, t_star, R):
    return 1 - R/k * np.arctan(np.tan(k) * np.exp(-t/t_star))

def find_closest_to_zero_index(array):
    absolute_values = np.abs(array)
    min_index = np.argmin(absolute_values)
    return min_index

def find_mean_value(vid, ratio=0.2):
    mean_values = []
    while True:
        ret, frame = vid.read()
        if not ret:
            break
        center_col = frame.shape[1] // 2
        left_col = int(center_col - (center_col * ratio))
        right_col = int(center_col + (center_col * ratio))
        frame[:, left_col:right_col] = 0
        
        mean_value = np.mean(frame)
        mean_values.append(mean_value)
    
    mean_values = np.array(mean_values)
    mean_values /= mean_values[-1]
    
    return mean_values

# Iterate through multiple runs
num_runs = 3  # Change this to the number of runs you have
for run in range(1, num_runs+1):
    video_path = f'/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Ultrasound_acoustofluidics/Video/Run {run}.mp4'
    timestamps_path = f'/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Ultrasound_acoustofluidics/Video/Run {run}_timestamps.txt'
    important_timestamps_path = f'/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Ultrasound_acoustofluidics/Video/Run {run}_important_timestamps.txt'

    # Load video, timestamps, and important timestamps
    vid = cv2.VideoCapture(video_path)
    timestamps = pd.read_csv(timestamps_path, header=None).to_numpy()
    important_timestamps = pd.read_csv(important_timestamps_path, header=None).to_numpy()
    frequency = timestamps[1]
    timestamps = timestamps[2:]

    # Find start time of acoustic focusing
    start_time = important_timestamps[0]
    t = timestamps - start_time
    start_index = find_closest_to_zero_index(timestamps)

    # Find mean value of each frame
    mean_values = find_mean_value(vid)
    popt, pcov = curve_fit(func, t[start_index:], mean_values[start_index:], p0=[1, 0.005], bounds=(0, np.inf))

    # Plot the mean values and the fitted function
    plt.figure(figsize=(10, 7.5), dpi=300)  # Set the figure size and dpi
    plt.plot(t, mean_values, label='Data')
    plt.plot(t, func(t, *popt), label='Fit')
    plt.axvline(x=t[start_index], color='r', linestyle='--', label='_nolabel_')
    plt.legend()
    plt.savefig(f'Run {run}.png')  # Save the plot as 'plot.png'
    plt.show()

    # Find the R_squared value
    residuals = mean_values[start_index:] - func(t[start_index:], *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((mean_values[start_index:] - np.mean(mean_values[start_index:]))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # Export the fitted parameters and the R_squared value to a csv file
    if run == 1:
        data = pd.DataFrame(columns=['Frequency', 't_star', 'R', 'R_squared'])
    data = data.append({'Frequency': frequency, 't_star': popt[0], 'R': popt[1], 'R_squared': r_squared}, ignore_index=True)
    if run == num_runs:
        data.to_csv('ImportantParameters.csv', index=False)
