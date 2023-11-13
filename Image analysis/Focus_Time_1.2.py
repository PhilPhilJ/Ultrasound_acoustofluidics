#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:06:32 2023

@author: joakimpihl
"""


#Load necessary packages
import cv2
import numpy as np
from matplotlib import pyplot as plt
#from matplotlib.widgets import Slider, Button
import pandas as pd
from scipy.optimize import curve_fit
from scipy import stats
import os

#Load video, background and timestamps for video
vid_num = 6 #choose video number - look at vid 0,1,2,6,7,8,9,10,11,12,13,14,15 for now
t_0 = 5.3 #np.array([]) # time that focussing starts - vid 0,1,2,6,7,8,9,10,11,12,13,14,15 for now

vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep/run'+str(vid_num)+'.mp4') #Loads the video
vid_back = cv2.VideoCapture('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep/run0.mp4') #Loads the background video
timestamps = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep/Time Stamps'+str(vid_num)+'.csv', delimiter=';', encoding='utf-8')
timestamps = timestamps['Frame time'].tolist()
freq = timestamps[0]
timestamps = np.array(timestamps[1:len(timestamps)])
timestamps = timestamps-timestamps[0]
timestamps = timestamps-t_0

index_left_side = 1370
index_right_side = 3078
#%%
#Define boundaries 
min_bound = int(round(index_left_side,0))
max_bound = int(round(index_right_side,0))
focus_point = 660 #Index compared to min bound
t_index_0 = np.where(np.isclose(timestamps, 0, atol=0.1))
mm_per_px = 400/(max_bound-min_bound) # conversion factor: um/px

###################################### Generate background and intensity matrix ######################################
ret, frame = vid.read()#Reads the fist frame
n_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) #Frames in video
#CHANGE DEPENDING ON WHICH VIDEO IS USED
timestamps = timestamps[0:n_frames] 
##################################
n_frames_back = int(vid_back.get(cv2.CAP_PROP_FRAME_COUNT)) #Frames in background video
plt.close('all') #Close all plots for good measure
#Define empty arrays to contain data
intensities = np.empty(np.size(frame[:,min_bound:max_bound], axis=1))
background = np.empty(np.size(frame[:,min_bound:max_bound], axis=1))

#Generate background
for i in range(n_frames_back-1):
    ret_2, back_frame = vid_back.read()
    back_frame = cv2.cvtColor(back_frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    back_frame = back_frame[:,min_bound:max_bound]
    back_frame_mean = np.mean(back_frame, axis=0)
    background = np.vstack([background, back_frame_mean])
    
#Generate matrix containing vertically meaned intensities
for i in range(n_frames-1):
    ret, frame = vid.read() #Reads the fist frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    frame = frame[:,min_bound:max_bound]
    frame_mean = np.mean(frame, axis=0)
    intensities = np.vstack([intensities, frame_mean])

background = background[1:np.size(background, axis=0),:]
mean_background = np.mean(background, axis=0)

intensities = intensities[1:np.size(intensities,axis=0),:]
timestamps = timestamps[1:len(timestamps)]

#Cleaning up memory
if 'vid' in globals():
    del frame, ret, ret_2, frame_mean, back_frame, back_frame_mean, vid, vid_back

intensities_sub_back = intensities - mean_background #Intensities subtracted background
I_rel = (-1)*intensities_sub_back/mean_background
# =============================================================================
# ######################################### 2/3D plot of intensities #########################################
# plt.close('all')
# fig, ax = plt.subplots(figsize=(10,10))
# img = ax.imshow(np.flipud(np.rot90(I_rel)), cmap='plasma_r', extent=[timestamps[0], timestamps[-1], 0, 400], interpolation='nearest') 
# 
# ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
# ax.set_ylabel(r'Position [$\mathrm{\mu m}$]', fontsize='17.5')
# ax.set_aspect(0.05)
# plt.rcParams.update({'font.size': 10})
# plt.colorbar(img, label='Relative drop in intensity', fraction=0.046, pad=0.04)
# 
# plt.show()
# 
# #3D plot
# =============================================================================
# =============================================================================
# plt.close('all')
# x = timestamps
# y = np.linspace(0, (max_bound-min_bound)*mm_per_px, (max_bound-min_bound))
# X, Y = np.meshgrid(x,y, indexing='xy')
# 
# plt.close('all')
# fig = plt.figure(figsize=(10,10))
# 
# ax = plt.axes(projection='3d')
# img3d = ax.plot_surface(X,Y,np.rot90(I_rel), cmap='plasma_r')
# ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
# ax.set_ylabel(r'Position [$\mathrm{\mu m}$]', fontsize='17.5')
# ax.set_zlabel(r'Relative drop in intensity', fontsize='17.5')
# fig.colorbar(img3d, label='Relative drop in intensity', fraction=0.046, pad=0.04, location='bottom')
# =============================================================================

#Define alpha region - The region which algae are focused into
alpha = 0.20
I_norm = np.empty([0])
w = np.size(intensities,axis=1) # width of channel

s1 = np.array([0, int(np.ceil(focus_point-alpha*w/2))]) #Index for section 1 going from px 0 to w/2-w*(1-alpha/2)
s2 = np.array([int(np.ceil(focus_point+alpha*w/2)), -1])

#Define max intensity - Max value is defined to be the mean of the background video intensity
I_0 = np.sum(intensities[t_index_0,s1[0]:s1[1]]) + np.sum(intensities[t_index_0,s2[0]:s2[1]])
I_max = np.sum(intensities[-1,s1[0]:s1[1]]) + np.sum(intensities[-1,s2[0]:s2[1]])

#For each timestamp figure out the intensity the intensity relative to I_max
for (i,j) in enumerate(timestamps):
    if i < np.size(intensities,axis=0):
        i_1 = np.sum(intensities[i, s1[0]:s1[1]])
        i_2 = np.sum(intensities[i, s2[0]:s2[1]])
        
        I_t = np.sum([i_1, i_2])
        I_norm = np.append(I_norm, I_t/I_max)

R = 1-I_0/I_max
k = np.pi*(1-alpha)/2

plt.close('all')
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(timestamps, I_norm, 'o')
plt.ylim([0.999*min(I_norm),1.001*max(I_norm)])

ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax.set_ylabel(r'$\frac{I}{I_{max}}$', fontsize='17.5')

I_norm_max = np.mean(I_norm[-5:-1])

ax.hlines(y=I_norm_max*0.9999, xmin=0, xmax=timestamps[-1])
ax.hlines(y=1-R, xmin=0, xmax=timestamps[-1])

fig2, ax2 = plt.subplots(figsize=(10,10))
img = ax2.imshow(np.flipud(np.rot90(I_rel)), cmap='plasma_r', extent=[timestamps[0], timestamps[-1], 0, 400], interpolation='nearest') 

######################################### Horizontal lines where diff. videos start #########################################
ax2.hlines(y=(w-s1[1])*mm_per_px, xmin=timestamps[0], xmax=timestamps[-1])
ax2.hlines(y=s2[0]*mm_per_px, xmin=timestamps[0], xmax=timestamps[-1])
ax2.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax2.set_ylabel(r'Position [$\mathrm{\mu m}$]', fontsize='17.5')
ax2.set_aspect(0.05)
plt.rcParams.update({'font.size': 10})
plt.colorbar(img, label='Relative drop in intensity', fraction=0.046, pad=0.04)

def func(t, t_star):
    return 1-R/k*np.arctan(np.tan(k)*np.exp(-t/t_star))

popt, pcov = curve_fit(func, timestamps, I_norm)

t_star = popt[0]

xdata_time = np.linspace(timestamps[0], timestamps[-1], 1000)
ydata = func(xdata_time, popt)
 
#Find R^2
residuals = I_norm - func(timestamps, popt) #Find residual
ss_res = np.sum(residuals**2) #Find residual sum of squares

ss_tot = np.sum((I_norm-np.mean(I_norm))**2) #Total sum of squares

r_squared = 1 - (ss_res / ss_tot) #R squared of fit

#%%
plt.close('all')
fig, ax = plt.subplots(figsize=(10,7.5))
ax.hlines(y=1-R/(1-alpha), xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax.hlines(y=1, xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax.plot(xdata_time, ydata, 'k--')
ax.plot(timestamps, I_norm, 'or')


ax.set_xlabel(r'Time ($\mathrm{s}$)', fontsize='17.5')
ax.set_ylabel(r'$\mathrm{I/I_{max}}$', fontsize='17.5')

focus_time = 0

for i,j in enumerate(ydata):
    if focus_time == 0 and j >= 0.9999*max(ydata):
        focus_time = xdata_time[i]
ax.legend(['Fit', 'Data'], loc='lower right', fontsize='15')
#%%
plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Resonance freq - Exp 2_1/'+str(freq)+' MHz.png', dpi=300, bbox_inches='tight')

df = pd.DataFrame({'Frequency (MHz)':[freq], 'Focusing time (99.99%)':[focus_time],'t_star':[t_star], 'alpha':[alpha], 'R':[R], 'r_squared':r_squared})

if os.path.exists('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Resonance freq - Exp 2_1/Resonance freq - Exp 2_1.csv') != True:
    df.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Resonance freq - Exp 2_1/Resonance freq - Exp 2_1.csv', sep=';')
else:
    df.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Resonance freq - Exp 2_1/Resonance freq - Exp 2_1.csv', sep=';', header=False, mode='a')
