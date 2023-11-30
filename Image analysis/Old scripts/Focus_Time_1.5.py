#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 13:09:28 2023

@author: joakimpihl
"""

#Load necessary packages
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

# Paths to files
vid_num = 4 #Video 0 through 16
path_vid = '/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep 2 sub back/run'+ str(vid_num)+'cropsubback.mp4'
path_imp_times = '/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep 2 sub back/Important times/Important times'+str(vid_num)+'.csv'
path_times = '/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep 2 sub back/Timestamps/Time Stamps'+str(vid_num)+'.csv'

# Load files
vid = cv2.VideoCapture(path_vid)
imp_times = pd.read_csv(path_imp_times, delimiter=';', encoding='utf-8') # [0] = focus start, [1] = focus stop
timestamps = pd.read_csv(path_times, delimiter=';', encoding='utf-8') # Timestamps start at index 2

# Manipulate csv files - Timescaling, and retrieve frequency information
timestamps, imp_times = timestamps['Frame time'].tolist(), np.array(imp_times['Important times'].tolist())
freq = timestamps[1] #Frequncy
timestamps = np.array(timestamps[2:len(timestamps)])
imp_times = np.array([imp_times[1], imp_times[2]])
t_index_0 = np.where(np.isclose(timestamps, imp_times[0], atol=0.1, rtol=0)) #Frame where focusing is started
if len(t_index_0) == 1:
    t_index_0 = int(t_index_0[0])
else:
    print('Error! Multiple starting indeces were found.')
timestamps, imp_times = timestamps[t_index_0:-1]-timestamps[t_index_0], imp_times-timestamps[t_index_0]
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
if len(timestamps) >= total_frames:
    timestamps = timestamps[0:total_frames] 
    #Reset frame count to the first valid frame
    vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
elif len(timestamps) < total_frames:
    print('Error there\'s more frames than timestamps.')
    Delta_frames = total_frames-len(timestamps)
    total_frames = len(timestamps)
    t_index_0 = Delta_frames

#Define empty arrays to contain data
intensities = np.empty([total_frames, px_width])

plt.close('all') #Close all plots for good measure

#Generate matrix containing vertically meaned intensities
for i in range(total_frames):
    vid.set(cv2.CAP_PROP_POS_FRAMES, i+Delta_frames)
    #print('Analyzing frame number: ' + str(int(vid.get(cv2.CAP_PROP_POS_FRAMES))))
    ret, frame = vid.read() #Reads the fist frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    frame_mean = np.mean(frame, axis=0)
    intensities[i] = frame_mean 

#Remove the first meaned frame as values are always 'weird'
intensities = intensities[1:np.size(intensities,axis=0),:]
timestamps = timestamps[1:len(timestamps)]
#Define alpha region - The region which algae are focused into
alpha = 0.20
I_norm = np.empty([len(timestamps)]) #normalised intensity - I/I_max

#Define the 2 sections where we measure the intensity change
s1 = np.array([0, int(np.ceil(px_width * (1 - alpha) * 1/2))]) #Index for section 1 going from px 0 to 1/2*w*(1-alpha)
s2 = np.array([int(np.ceil(px_width * (1+alpha) * 1/2)), -1]) #Index for section 2 going from px 1/2*w*(1+alpha) to w


#Define max intensity - Max value is defined to be the sum of mean intensities of the last frame
I_0 = np.sum(intensities[t_index_0,s1[0]:s1[1]]) + np.sum(intensities[t_index_0,s2[0]:s2[1]]) # Intensity when focussing was started
I_max = np.sum(intensities[-1,s1[0]:s1[1]]) + np.sum(intensities[-1,s2[0]:s2[1]]) # Max intensity
#R = 1 - I_0/I_max # Relative reduction in intensity
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

popt, pcov = curve_fit(func, timestamps, I_norm) #Fitting
t_star = popt[0] #Defining the best value of the fitting parameter
R = popt[1] #Also fitting for R

#Generate fitting data to overlay experimental data
xdata_time = np.linspace(timestamps[0], timestamps[-1], 1000)
ydata = func(xdata_time, *popt)

#Make plot of experimental data and plot
plt.close('all')
fig, ax = plt.subplots(figsize=(10,7.5))
ax.hlines(y=1-R/(1-alpha), xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax.hlines(y=1, xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax.plot(xdata_time, ydata, 'k--')
ax.plot(timestamps, I_norm, 'or')
plt.title('Run '+str(vid_num)+' and freq. ' + str(freq)+r' MHz (Fitting parameters: $t^*$ and R)', fontsize='20')

ax.set_xlabel(r'Time ($\mathrm{s}$)', fontsize='17.5')
ax.set_ylabel(r'$\mathrm{I/I_{max}}$', fontsize='17.5')

focus_time = 0 #Will be redefined to the focussing time of the algae

for i,j in enumerate(ydata):
    if focus_time == 0 and j >= 0.9999*max(ydata):
        focus_time = xdata_time[i]
ax.legend(['Fit', 'Data'], loc='lower right', fontsize='15')


plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep 2 sub back/Fits (t_star + R)/run '+str(vid_num)+' freq.:'+str(freq)+' MHz.png', dpi=300, bbox_inches='tight')
