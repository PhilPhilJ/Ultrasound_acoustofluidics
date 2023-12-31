#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:43:09 2023

@author: joakimpihl
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd

# =============================================================================
# vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/190923/Algae_Vid_exp_3_1909.mp4') #Loads the video
# vid_back = cv2.VideoCapture('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/190923/Algae_Vid_background_2_1909.mp4') #Loads the background video
# =============================================================================
vid = cv2.VideoCapture('/Volumes/Elements/Algae experiment 4/18_run/focus_18.mp4') #Loads the video
vid_back = cv2.VideoCapture('/Volumes/Elements/Algae experiment 4/18_run/backgroung_18.mp4') #Loads the background video
timestamps = pd.read_csv('/Volumes/Elements/Algae experiment 4/Time Stamps - sweep', delimiter=';')
timestamps = timestamps['Frequency sweep'].tolist()
timestamps = np.array(timestamps[1:len(timestamps)])
timestamps = timestamps-timestamps[0]

#%%
#Define boundaries found using Image_crop_v3.py
min_bound = 613 #1405
max_bound = 2567 #3545
mm_per_px = 400/(max_bound-min_bound) # um/px
#Reads the fist frame
ret, frame = vid.read()
n_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
n_frames_back = int(vid_back.get(cv2.CAP_PROP_FRAME_COUNT))
plt.close('all')
intensities = np.empty(np.size(frame[:,min_bound:max_bound], axis=1))
background = np.empty(np.size(frame[:,min_bound:max_bound], axis=1))

#Generate background
for i in range(n_frames_back):
    ret_2, back_frame = vid_back.read()
    back_frame = cv2.cvtColor(back_frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    back_frame = back_frame[:,min_bound:max_bound]
    back_frame_mean = np.mean(back_frame, axis=0)
    background = np.vstack([background, back_frame_mean])

#Generate matix containing vertically meaned intensities
for i in range(n_frames-1):
    ret, frame = vid.read() #Reads the fist frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    frame = frame[:,min_bound:max_bound]
    frame_mean = np.mean(frame, axis=0)
    intensities = np.vstack([intensities, frame_mean])

timestamps = timestamps[(len(timestamps)-n_frames):len(timestamps)]
intensities = intensities[1:np.size(intensities,axis=0),:]
mean_background = np.mean(background[1:np.size(background, axis=0)], axis=0)
background = background[1:np.size(background, axis=0),:]

#Cleaning up memory
del frame, ret, ret_2, frame_mean, back_frame, back_frame_mean, vid, vid_back

#%%
plt.close('all')

fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
back_over_time = np.zeros(n_frames_back)

def update(val):
    frame_val = int(Slider_val.val)-1
    plot_of_background.set_ydata(background[frame_val,:])
    fig.canvas.draw_idle()


fig.set_size_inches(30/2.54, 25/2.54)
fig.suptitle('Plot of background intensity, background intensity over time, and mean background intensity', fontsize='15') 
# Set common labels
fig.text(0.5, 0.025, 'X-position [px]', ha='center', va='center', fontsize='12.5')
fig.text(0.025, 0.5, 'Intensity [0:255]', ha='center', va='center', rotation='vertical', fontsize='12.5')
fig.tight_layout(pad=3)

ax1.plot(np.arange(min_bound,max_bound), mean_background, color='black', linestyle='dashdot')
plot_of_background, = ax1.plot(np.arange(min_bound,max_bound), background[0,:], color='r')
ax_slider = plt.axes([0.125, 0.915, 0.80, 0.04], facecolor="red")
Slider_val = Slider(ax_slider, 'Frame', 1, np.size(background, axis=0), valinit=1, valstep=1)
Slider_val.on_changed(update)
ax1.set_title('Background intensity', fontsize='12.5')
ax1.set_ylim(np.mean(mean_background)*0.95, np.mean(mean_background)*1.05)
#ax1.set_ylim([np.min(mean_background)-1, np.max(mean_background)+1])


for i in range(n_frames_back):
    ax2.plot(np.arange(min_bound,max_bound), background[i,:], color='r')
    back_over_time[i] = np.mean(background[i,1430:1800])
    
ax2.set_title('Background intensity over time', fontsize='12.5')

ax3.plot(np.arange(min_bound,max_bound), mean_background, color='r')
ax3.set_title('Mean background', fontsize='12.5')

#plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/background_plots.png', dpi=300) #Save the plot
#%%
# =============================================================================
# plt.close('all')
# plt.plot(np.arange(n_frames_back)/18, back_over_time)
# plt.title('Background intensity over time [2680:3050]', fontsize='20')
# plt.xlabel('Time [s]', fontsize='15')
# plt.ylabel('Intensity [0:255]', fontsize='15')
# 
# plt.show()
# 
# =============================================================================

#%%
plt.close('all')
del plot_of_background
#%%

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, sharey=False)


def update_2(val):
    frame_val = int(Slider_val.val)-1
    plot_of_intensities.set_ydata(intensities[frame_val,:])
    plot_of_intensities_2.set_ydata(intensities[frame_val,:]-mean_background)
    fig.canvas.draw_idle()


fig.set_size_inches(30/2.54, 25/2.54)
fig.suptitle('Plot of Intensity, intensity over time, and mean intensity', fontsize='15') 
# Set common labels
fig.text(0.5, 0.025, 'X-position [px]', ha='center', va='center', fontsize='12.5')
fig.text(0.025, 0.5, 'Intensity [0:255]', ha='center', va='center', rotation='vertical', fontsize='12.5')
fig.tight_layout(pad=3)

ax1.plot(np.arange(min_bound,max_bound), mean_background, color='black', linestyle='dashdot')
plot_of_intensities, = ax1.plot(np.arange(min_bound,max_bound), intensities[0,:], color='r')
ax_slider = plt.axes([0.125, 0.915, 0.80, 0.04], facecolor="red")
Slider_val = Slider(ax_slider, 'Frame', 1, np.size(intensities, axis=0), valinit=1, valstep=1)
Slider_val.on_changed(update_2)
ax1.set_title('Intensity', fontsize='12.5')
ax1.set_ylim([np.mean(mean_background)*0.875, np.mean(mean_background)*1.075])
#ax1.set_ylim([np.min(mean_background)-1, np.max(mean_background)+1])


for i in range(np.size(intensities, axis=0)):
    ax2.plot(np.arange(min_bound,max_bound), intensities[i,:], color='r')
ax2.set_title('Intensity over time', fontsize='12.5')


ax3.plot(np.arange(min_bound,max_bound), mean_background-mean_background, color='black', linestyle='dashdot')
plot_of_intensities_2, = ax3.plot(np.arange(min_bound,max_bound), intensities[0,:]-mean_background, color='r')
Slider_val.on_changed(update_2)
ax3.set_title('Intensity with background subtracted', fontsize='12.5')
ax3.set_ylim([np.min(intensities-mean_background)-1, np.max(intensities-mean_background)+1])


for i in range(np.size(intensities, axis=0)):
    ax4.plot(np.arange(min_bound,max_bound), intensities[i,:]-mean_background, color='r')
ax4.set_title('Intensity over time with background subtracted', fontsize='12.5')


#plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Figure_2_2.png', dpi=300)
#%%
# intensity plot

intensities_sub_back = intensities - mean_background
I_rel = intensities_sub_back/mean_background
#I_rel_2 = intensities/np.mean(mean_background)

del fig, ax1, ax2, ax3, ax4, plot_of_intensities, plot_of_intensities_2, Slider_val, ax_slider
#%%
plt.close('all')
fig, ax = plt.subplots(figsize=(10,10))
#img = ax.imshow(np.transpose(intensities_sub_back), cmap='viridis', extent=[0, n_frames/18, 0, (max_bound-min_bound)*mm_per_px], interpolation='nearest') #Play around with the cmaps to finde the best one
img = ax.imshow(np.flipud(np.rot90(-1*I_rel)), cmap='plasma_r', extent=[timestamps[0], timestamps[len(timestamps)-1], 0, (max_bound-min_bound)*mm_per_px], interpolation='nearest') #Play around with the cmaps to finde the best one
#img = ax.imshow(np.transpose(I_rel), cmap='viridis', extent=[0, np.ceil(n_frames/18), 0, (max_bound-min_bound)*mm_per_px], interpolation='nearest') #Play around with the cmaps to finde the best one
ax.vlines(x=timestamps[int(n_frames/5)], ymin=0, ymax=(max_bound-min_bound)*mm_per_px)
ax.vlines(x=timestamps[int(n_frames*2/5)], ymin=0, ymax=(max_bound-min_bound)*mm_per_px)
ax.vlines(x=timestamps[int(n_frames*3/5)], ymin=0, ymax=(max_bound-min_bound)*mm_per_px)
ax.vlines(x=timestamps[int(n_frames*4/5)], ymin=0, ymax=(max_bound-min_bound)*mm_per_px)
ax.set_title('Some title', fontsize='25')
ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax.set_ylabel(r'Position [$\mathrm{\mu m}$]', fontsize='17.5')
ax.set_aspect(0.2)
plt.rcParams.update({'font.size': 10})
plt.colorbar(img, label='Relative drop in intensity', fraction=0.046, pad=0.04)

#%%
#3D plot
plt.close('all')
x = timestamps#np.linspace(0,n_frames/18, n_frames)
y = np.linspace(0, (max_bound-min_bound)*mm_per_px, (max_bound-min_bound))
X, Y = np.meshgrid(x,y, indexing='xy')
#X = X[0:np.size(X,axis=0)-1,:]
#Y = Y[0:np.size(Y,axis=0)-1,:]
X = X[:,0:np.size(X,axis=1)-1]
Y = Y[:,0:np.size(Y,axis=1)-1]
#%%
plt.close('all')
fig = plt.figure(figsize=(10,10))

ax = plt.axes(projection='3d')
img3d = ax.plot_surface(X,Y,-1*np.rot90(I_rel), cmap='plasma_r')
ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax.set_ylabel(r'Position [$\mathrm{\mu m}$]', fontsize='17.5')
ax.set_zlabel(r'Relative drop in intensity', fontsize='17.5')
ax.set_title('Some other title', fontsize='25')
fig.colorbar(img3d, label='Relative drop in intensity', fraction=0.046, pad=0.04, location='bottom')

