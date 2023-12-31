#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 15:52:47 2023

@author: joakimpihl
"""

#Load necessary packages
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os

# Paths to files
#vid_num = 15 #Video 0 through 52
path_out ='/Users/joakimpihl/Desktop/Contrast vid result/'
for vid_num in range(11,14):
    path_vid = '/Users/joakimpihl/Desktop/Contrast vid/run'+ str(vid_num)+'.mp4'
    path_imp_times = '/Users/joakimpihl/Desktop/Contrast vid/Important times'+str(vid_num)+'.csv'
    path_times = '/Users/joakimpihl/Desktop/Contrast vid/Time Stamps'+str(vid_num)+'.csv'
    
    # Load files
    vid = cv2.VideoCapture(path_vid)
    imp_times = pd.read_csv(path_imp_times, delimiter=';', encoding='utf-8')['Important times'].tolist() # [0] = focus start, [1] = focus stop
    timestamps = pd.read_csv(path_times, delimiter=';', encoding='utf-8')['Frame time'].iloc[2:].tolist() # Timestamps start at index 2
    freq = pd.read_csv(path_times, delimiter=';', encoding='utf-8')['Frame time'].iloc[1].tolist() #Frequncy in MHz
    
    # Manipulate csv files - Timescaling, and retrieve frequency information
    t_index_0 = None
    t_index_end = None
    for i, ts in enumerate(timestamps):
        if np.isclose(ts, imp_times[1], atol=0.01, rtol=0):
            if t_index_0 is None:
                t_index_0 = i
            else:
                raise ValueError('Error! Multiple starting indices were found.')
        if np.isclose(ts, imp_times[2], atol=0.01, rtol=0):
            if t_index_end is None:
                t_index_end = i
            else:
                raise ValueError('Error! Multiple starting indices were found.')
    
    if t_index_0 is not None:
        timestamps = np.array(timestamps) - timestamps[t_index_0]
        imp_times = np.array(imp_times) - timestamps[t_index_0]
    else:
        raise ValueError('Error! No starting index found.')
    ###################################### Generate intensity matrix ######################################
    ret, frame = vid.read()#Reads the fist frame
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) #Frames in video
    
    # Scaling information
    px_width = np.size(frame, axis=1) #Width of video in px
    px_height = np.size(frame, axis=0) #Height of video in px
    mm_per_px = 400/px_width # conversion factor: um/px
    width = px_width * mm_per_px #um
    height = px_height * mm_per_px #um
    
    #if there's a missmatch between the number of frames and the number of timestamps
    if len(timestamps) != total_frames:
        raise ValueError('The number of timestamps doens\'t match the number of frames recorded.')
    
    #Define empty arrays to contain data
    intensities = np.empty([total_frames, px_width])
    
    plt.close('all') #Close all plots for good measure

    #Generate matrix containing vertically meaned intensities
    for i in range(total_frames):
        vid.set(cv2.CAP_PROP_POS_FRAMES, i)
        print('Analyzing frame number: ' + str(int(vid.get(cv2.CAP_PROP_POS_FRAMES))))
        ret, frame = vid.read() #Reads the fist frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
        frame_mean = np.mean(frame, axis=0)
        intensities[i] = frame_mean 
    
    #Remove the first meaned frame as values are always 'weird'
    intensities = np.delete(intensities, 0, 0)
    timestamps = np.delete(timestamps, 0)
    
    #Define alpha region - The region which algae are focused into
    alpha = 0.20
    I_norm = np.empty([len(timestamps)]) #normalised intensity - I/I_max
    
    #Define the 2 sections where we measure the intensity change
    s1 = np.array([0, int(np.ceil(px_width * (1 - alpha) * 1/2))]) #Index for section 1 going from px 0 to 1/2*w*(1-alpha)
    s2 = np.array([int(np.ceil(px_width * (1+alpha) * 1/2)), -1]) #Index for section 2 going from px 1/2*w*(1+alpha) to w
    
    
    #Define max intensity - Max value is defined to be the sum of mean intensities of the last frame
    I_0 = np.sum(intensities[t_index_0,s1[0]:s1[1]]) + np.sum(intensities[t_index_0,s2[0]:s2[1]]) # Intensity when focussing was started
    I_max = np.sum(intensities[-1,s1[0]:s1[1]]) + np.sum(intensities[-1,s2[0]:s2[1]]) # Max intensity
    R_data = 1 - I_0/I_max # Relative reduction in intensity
    k = np.pi*(1-alpha)/2 #Defining a constant k
    
    #For each timestamp figure out the intensity the intensity relative to I_max
    for i in range(len(timestamps)):
        if i < np.size(intensities,axis=0):
            i_1 = np.sum(intensities[i, s1[0]:s1[1]])
            i_2 = np.sum(intensities[i, s2[0]:s2[1]])
            
            I_t = np.sum([i_1, i_2])
            I_norm[i] = I_t/I_max
            
    ###################################### Make a fit to the data ######################################
    def func(t, t_star, R): #Define function which data is fitted to
        return 1-R/k*np.arctan(np.tan(k)*np.exp(-t/t_star))
    
    popt, pcov = curve_fit(func, timestamps[t_index_0:t_index_end+1], I_norm[t_index_0:t_index_end+1]) #Fitting
    t_star = popt[0] #Defining the best value of the fitting parameter
    R_fit = popt[1] #Also fitting for R
    sigma = np.sqrt(pcov[0,0]) #Standard deviation on t_star
    N_samples = len(timestamps[t_index_0:t_index_end+1])
    
    # Find r^2 - https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit
    residuals = I_norm[t_index_0:t_index_end+1] - func(timestamps[t_index_0:t_index_end+1], *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((I_norm[t_index_0:t_index_end+1]-np.mean(I_norm[t_index_0:t_index_end+1]))**2)
    r_squared = 1 - (ss_res / ss_tot)
    # r^2 calculation done
    
    #Generate fitting data to overlay experimental data
    xdata_time = np.linspace(timestamps[0], timestamps[-1], 1000)
    ydata = func(xdata_time, *popt)
    
    #Make plot of experimental data and plot
    delta_y=R_fit/(1-alpha)
    plt.close('all')
    fig, ax = plt.subplots(figsize=(10,7.5))
    ax.hlines(y=1-R_fit/(1-alpha), xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
    ax.hlines(y=1, xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
    ax.plot(timestamps[t_index_0:t_index_end+1], I_norm[t_index_0:t_index_end+1], 'or')
    ax.plot(timestamps[0:t_index_0], I_norm[0:t_index_0], color='black', marker='o')
    ax.plot(timestamps[t_index_end+1:-1], I_norm[t_index_end+1:-1], color='black', marker='o')
    ax.plot(xdata_time, ydata, 'k--')
    #ax.vlines(x=timestamps[t_index_0], ymin=min(I_norm)-0.2*delta_y, ymax=max(I_norm)+0.1*delta_y, color='black', alpha=0.5, linestyle='dashdot', label='_nolegend_')
    #ax.vlines(x=timestamps[t_index_end], ymin=min(I_norm)-0.2*delta_y, ymax=max(I_norm)+0.1*delta_y, color='black', alpha=0.5, linestyle='dashdot', label='_nolegend_')
    plt.title('Run '+str(vid_num)+' and freq. ' + str(round(freq,3))+r' MHz (Fitting parameters: $t^*$ and R)', fontsize='20')
    
    ax.set_xlabel(r'Time ($\mathrm{s}$)', fontsize='17.5')
    ax.set_ylabel(r'$\mathrm{I/I_{max}}$', fontsize='17.5')
    
    plt.savefig(path_out + 'Plots/run '+str(vid_num)+' freq. '+str(round(freq, 3))+' MHz.png', dpi=300, bbox_inches='tight')
    
    df = pd.DataFrame({'Frequency (MHz)':[freq], 't_star':[t_star], 'alpha':[alpha], 'R (Fit)':[R_fit], 'R (Data)':[R_data], 'St dev on t_star':[sigma], 'Sample size':[N_samples], 'R squared':[r_squared]})
    
    if os.path.exists(path_out + 'Resonance freq.csv') != True:
        df.to_csv(path_out + 'Resonance freq.csv', sep=',')
    else:
        df.to_csv(path_out + 'Resonance freq.csv', sep=',', header=False, mode='a')

#%%
plt.close('all')

# Example array
data = I_norm

# Calculate differences between consecutive elements
differences = np.diff(data)

# Set a threshold for what defines a 'jump'
threshold = 10**(-4)*5  # You can adjust this value based on your data characteristics

# Find indexes where the difference exceeds the threshold
jump_indexes = np.where(np.abs(differences) > threshold)[0] + 1  # Adding 1 to account for np.diff

# Create a figure and axis
fig, ax = plt.subplots(figsize=(8, 5))
line, = ax.plot(data, marker='o', linestyle='-', color='blue', label='Data Points')
ax.set_title("Identifying Jumps in Data")
ax.set_xlabel("Index")
ax.set_ylabel("Value")

# Highlight points where the jump occurs
scatter = ax.scatter(jump_indexes, data[jump_indexes], color='red', s=100, label='Jump Points')

# Function to handle mouse hover event
def on_hover(event):
    if event.inaxes == ax:
        for i, point in enumerate(data):
            if abs(event.xdata - i) < 0.1:  # Checking proximity to the data points
                jump_size = round(differences[i - 1], 5) if i > 0 else None
                point_value = round(point, 5)
                plt.gca().set_title(f"Index: {i}, Value: {point_value}, Jump Size: {jump_size}")
                fig.canvas.draw_idle()
                break

# Connect the hover event to the figure
fig.canvas.mpl_connect('motion_notify_event', on_hover)

plt.legend()
plt.grid(True)
plt.show()

#%%
kappa = 0.0006815391424205656
upper_indeces = np.concatenate((range(8,98), range(132, 148), range(261,328), range(389,426)))

I_norm_2 = np.copy(I_norm)

I_norm_2[upper_indeces] = I_norm[upper_indeces]-kappa

plt.close('all')

fig, ax = plt.subplots(figsize=(10,7.5))
ax.plot(timestamps[t_index_0:t_index_end+1], I_norm_2[t_index_0:t_index_end+1], 'or')
ax.plot(timestamps[0:t_index_0], I_norm_2[0:t_index_0], color='black', marker='o')
ax.plot(timestamps[t_index_end+1:-1], I_norm_2[t_index_end+1:-1], color='black', marker='o')

#%%
popt2, pcov2 = curve_fit(func, timestamps[t_index_0:t_index_end+1], I_norm_2[t_index_0:t_index_end+1]) #Fitting

residuals2 = I_norm_2[t_index_0:t_index_end+1] - func(timestamps[t_index_0:t_index_end+1], *popt2)
ss_res2 = np.sum(residuals2**2)
ss_tot2 = np.sum((I_norm_2[t_index_0:t_index_end+1]-np.mean(I_norm_2[t_index_0:t_index_end+1]))**2)
r_squared_2 = 1 - (ss_res2 / ss_tot2)

#Generate fitting data to overlay experimental data
ydata2 = func(xdata_time, *popt2)

plt.close('all')

fig, ax = plt.subplots(figsize=(10,7.5))
ax.scatter(timestamps[I_norm_2 != I_norm_2[upper_indeces]], I_norm_2[I_norm_2 != I_norm_2[upper_indeces]], marker='o', color='red')
ax.scatter(timestamps[upper_indeces], I_norm_2[upper_indeces], marker='o', color='blue')
ax.plot(xdata_time, ydata2, linestyle='dashdot', color='black')

plt.title('Run '+str(vid_num)+' and freq. ' + str(round(freq,3))+r' MHz (Fitting parameters: $t^*$ and R)', fontsize='20')
    
ax.set_xlabel(r'Time ($\mathrm{s}$)', fontsize='17.5')
ax.set_ylabel(r'$\mathrm{I/I_{max}}$', fontsize='17.5')