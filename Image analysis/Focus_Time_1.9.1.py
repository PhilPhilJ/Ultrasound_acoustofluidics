#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 14:06:19 2023

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
path_out ='/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/'
for vid_num in range(2,3):
    path_vid = '/Users/joakimpihl/Desktop/run1Frequency 1.91Hz/frequency1.91.mp4' #'/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Experiments/Focus sweep 6 edited/run'+ str(vid_num)+'.mp4'
    path_imp_times = '/Users/joakimpihl/Desktop/run1Frequency 1.91Hz/Important times1.91Hz.csv' #'/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Experiments/Focus sweep 6 edited/Important times'+str(vid_num)+'.csv'
    path_times = '/Users/joakimpihl/Desktop/run1Frequency 1.91Hz/timestamps.csv' #'/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Experiments/Focus sweep 6 edited/Time Stamps'+str(vid_num)+'.csv'
    
    # Load files
    vid = cv2.VideoCapture(path_vid)
    imp_times = pd.read_csv(path_imp_times, delimiter=';', encoding='utf-8')['Important times'].tolist() # [0] = focus start, [1] = focus stop
    timestamps = pd.read_csv(path_times, delimiter=';', encoding='utf-8')['Frame time'].iloc[2:].tolist() # Timestamps start at index 2
    freq = pd.read_csv(path_times, delimiter=';', encoding='utf-8')['Frame time'].iloc[1].tolist() #Frequncy in MHz
    
    #The switch valve for experiment is closed after 30s
    # Manipulate csv files - Timescaling, and retrieve frequency information
    t_index_switch = None
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
        if np.isclose(ts, imp_times[1]-10, atol=0.02, rtol=0):
            if t_index_switch is None:
                t_index_switch = i
            else:
                raise ValueError('Error! Multiple starting indices were found.')
    
    if t_index_0 is not None:
        timestamps = np.array(timestamps) - timestamps[t_index_0]
        imp_times = np.array(imp_times) - timestamps[t_index_0]
    else:
        raise ValueError('Error! No starting index found.')
        
    timestamps = timestamps[t_index_switch:len(timestamps)]
    t_index_0 = t_index_0-t_index_switch
    t_index_end = t_index_end - t_index_switch
    #%%
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
    if len(timestamps) != total_frames-t_index_switch:
        raise ValueError('The number of timestamps doens\'t match the number of frames recorded.')
    
    #Define empty arrays to contain data
    intensities = np.empty([total_frames-t_index_switch, px_width])
    
    plt.close('all') #Close all plots for good measure

    #Generate matrix containing vertically meaned intensities
    for i in range(t_index_switch,total_frames):
        vid.set(cv2.CAP_PROP_POS_FRAMES, i)
        print('Analyzing frame number: ' + str(int(vid.get(cv2.CAP_PROP_POS_FRAMES))))
        ret, frame = vid.read() #Reads the fist frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
        frame_mean = np.mean(frame, axis=0)
        intensities[i-t_index_switch] = frame_mean 
    
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


plt.close('all')
#%%
I_norm_2 = np.copy(I_norm)
timestamps = timestamps[0:-1]
#%%
def func(t, t_star, R): #Define function which data is fitted to
    return 1-R/k*np.arctan(np.tan(k)*np.exp(-t/t_star))

popt, pcov = curve_fit(func, timestamps, I_norm_2) #Fitting - Use all data or still just truncated data set? [t_index_0:t_index_end] [t_index_0:t_index_end]

#Fitting parameters are defined
t_star = popt[0]
R_fit = popt[1]
sigma = pcov[0,0]
N_samples = len(timestamps[t_index_0:t_index_end+1])
delta_y=R_fit/(1-alpha)

residuals = I_norm_2[t_index_0:t_index_end] - func(timestamps[t_index_0:t_index_end], *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((I_norm_2[t_index_0:t_index_end]-np.mean(I_norm_2[t_index_0:t_index_end]))**2)
r_squared = 1 - (ss_res / ss_tot)

#Generate fitting data to overlay experimental data
xdata_time = np.linspace(timestamps[0], timestamps[-1], 1000)
ydata = func(xdata_time, *popt)

plt.close('all')

t_star_e = format(t_star, ".1e")
R_fit_e = format(R_fit, ".1e")

fig, ax = plt.subplots(figsize=(10,7.5))
#ax.vlines(x=timestamps[t_index_0], ymin=0, ymax=2, color='black', alpha=0.5, linestyle='dashdot', label='_nolegend_')
#ax.vlines(x=timestamps[t_index_end], ymin=0, ymax=2, color='black', alpha=0.5, linestyle='dashdot', label='_nolegend_')
ax.hlines(y=1-R_fit/(1-alpha), xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax.hlines(y=1, xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax.scatter(timestamps, I_norm_2, marker='o', color='red', label='Data')
ax.plot(xdata_time, ydata, linestyle='dashdot', color='black', label=f'Fit ($t^*$ = {t_star_e}, R = {R_fit_e})')

plt.ylim((0.998, 1.004))

plt.title('Run '+str(vid_num)+' and freq. ' + str(round(freq,3))+r' MHz (Fitting parameters: $t^*$ and R)', fontsize='20')
    
ax.set_xlabel(r'Time ($\mathrm{s}$)', fontsize='17.5')
ax.set_ylabel(r'$\mathrm{I/I_{max}}$', fontsize='17.5')

plt.legend(loc='lower right')

#%%
#plt.savefig(path_out + 'Plots/run '+str(vid_num)+' freq. '+str(round(freq, 3))+' MHz.png', dpi=300, bbox_inches='tight')
    
#df = pd.DataFrame({'Frequency (MHz)':[freq], 't_star':[t_star], 'alpha':[alpha], 'R (Fit)':[R_fit], 'R (Data)':[R_data], 'St dev on t_star':[sigma], 'Sample size':[N_samples], 'R squared':[r_squared]})

df_I = pd.DataFrame({'Timestamps':timestamps, 'Normalized intensity':I_norm_2 })
df_I.to_csv(path_out + 'Corrected I_norm/corrected I_norm run'+str(vid_num)+'.csv', sep=',')
    
#if os.path.exists(path_out + 'Resonance freq_v2.csv') != True:
#    df.to_csv(path_out + 'Resonance freq_v2.csv', sep=',')
#else:
#    df.to_csv(path_out + 'Resonance freq_v2.csv', sep=',', header=False, mode='a')


