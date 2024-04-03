import cv2, os, sys
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import time

sys.path.append('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Ultrasound_acoustofluidics/')

# Define functions
def func(t, t_star, R, ratio=0.2):
    k = np.pi*(1-ratio)/2
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
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        center_col = frame.shape[1] // 2
        left_col = int(center_col - (center_col * ratio))
        right_col = int(center_col + (center_col * ratio))
        cropped_frame = np.concatenate([frame[:, :left_col], frame[:, right_col:]], axis=1)
        
        mean_value = np.mean(cropped_frame)
        mean_values.append(mean_value)
    
    mean_values = np.array(mean_values)
    mean_values /= mean_values[-1]
    
    return mean_values

# Iterate through multiple runs
num_runs = 200  # Change this to the number of runs you have
start_time_1 = time.time()
for run in range(0, num_runs):
    video_path = f'/Users/joakimpihl/Desktop/Run (20:03:24)/run {run}.mp4'
    timestamps_path = f'/Users/joakimpihl/Desktop/Run (20:03:24)/Time Stamps {run}.csv'
    important_timestamps_path = f'/Users/joakimpihl/Desktop/Run (20:03:24)/Important times {run}.csv'

    # Load video, timestamps, and important timestamps
    vid = cv2.VideoCapture(video_path)
    timestamps = pd.read_csv(timestamps_path, delimiter=';', encoding='utf8').to_numpy(dtype=float)
    important_timestamps = pd.read_csv(important_timestamps_path, delimiter=';').to_numpy(dtype=float)
    frequency = timestamps[2, 0]
    timestamps = timestamps[2:, 2]

    # Find start time of acoustic focusing
    start_time = important_timestamps[1, 2]
    print(f'Start time: {start_time}')
    print(f'Frequency: {frequency}')
    print(np.shape(timestamps))
    t = timestamps - start_time
    start_index = find_closest_to_zero_index(t)

    # Find mean value of each frame
    mean_values = find_mean_value(vid)
    popt, pcov = curve_fit(func, t[start_index:], mean_values[start_index:], p0=[1, 0.005], bounds=([0, 0], [100, 1]))

    # Plot the mean values and the fitted function
    plt.figure(figsize=(10, 7.5), dpi=300)  # Set the figure size and dpi
    plt.plot(t, mean_values, 'ro',label='Data')
    plt.plot(t, func(t, *popt), color='black', label='Fit')
    plt.axvline(x=t[start_index], color='black', linestyle='--', label='_nolabel_')
    plt.legend(loc='lower right')
    plt.savefig(f'/Users/joakimpihl/Desktop/Run result/Plots/Run {run}.png')  # Save the plot as 'plot.png'
    plt.show()

    # Find the R_squared value
    residuals = mean_values[start_index:] - func(t[start_index:], *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((mean_values[start_index:] - np.mean(mean_values[start_index:]))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # Export the fitted parameters and the R_squared value to a csv file
    data = pd.DataFrame({'Frequency': [frequency], 't_star': [popt[0]], 'R': [popt[1]], 'R_squared': [r_squared]})
    if run == 0:
        data.to_csv('/Users/joakimpihl/Desktop/Run result/ImportantParameters.csv', header=True)
    else:
        data.to_csv('/Users/joakimpihl/Desktop/Run result/ImportantParameters.csv', header=False, mode='a')
end_time = time.time()
print(f'Time elapsed: {end_time - start_time_1} seconds')