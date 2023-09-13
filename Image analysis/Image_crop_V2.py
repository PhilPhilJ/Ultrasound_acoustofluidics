#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 12:44:54 2023

@author: joakimpihl
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button

#vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video
vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video


#Reads the fist frame
ret, frame = vid.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale



#average the video along y-dricetion so that we get an 1D array/vector
frame_1d = np.array(np.mean(frame, axis=0))
#grad = abs(np.diff(frame_1d))

#Creates a y-averaged image
ave_frame = np.round(np.tile(frame_1d, (len(frame_1d),1)))/255 #Frame avereaged along y-driection

threshold, _ = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) 

####################################### Plotting intensities overlayed image of channel #######################################
# Cv2 makes a guess for An option to change the inital threshold value has been added
# The threshold should be chosen such that the entire channel intensity is below the threshold intensity

fig, ax1 = plt.subplots()

ax1.set_xlabel('x-direction [px]') #Image of channel
ax1.set_ylabel('y-dricetion [px]')
ax1.imshow(frame,cmap='gray')

ax2 = ax1.twinx() #Intensities
ax2.set_ylabel('Intensity [0;255]')
ax2.plot(np.arange(0, len(frame_1d)), frame_1d, color='r')

#ax3 = ax1.twinx() #Intensities
ax3 = ax2.twiny()
ax3.axis('off')
thresh_line, = ax3.plot(np.arange(0, len(frame_1d)), np.array([threshold]*len(frame_1d)), color='b', label='Threshold = ' + str(threshold))
ax3.legend()


# Make a horizontal slider to control the frequency.
axthresh = fig.add_axes([0.2, 0.01, 0.65, 0.01])
thresh_slider = Slider(ax=axthresh, label='Threshold', valmin=0, valmax=255, valinit=threshold)

# The function to be called anytime a slider's value changes
def update(val):
    global slider_val
    slider_val = val
    thresh_line.set_ydata(np.array([val]*len(frame_1d)))
    fig.canvas.draw_idle()

# register the update function with each slider
thresh_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to accept the slider value.
accept_val = fig.add_axes([0.85, 0.05, 0.1, 0.04])
button = Button(accept_val, 'Accept', hovercolor='0.975')
    
def assign(event): #A function that assigns the threshold value given by the slider
    globals()['threshold'] = globals()['slider_val']
    print('The new threshold has been set to: ' + str(round(globals()['threshold'],1)))
    plt.close(fig)

button.on_clicked(assign)

fig.tight_layout()
plt.show()

##############################################################################################################################

#Everything above threshold limit is white, and everything below is made black

frame_bw = np.copy(frame)

frame_bw[frame_bw<threshold] = 0
frame_bw[frame_bw>=threshold] = 255

frame_mean = np.mean(frame_bw, axis=0)
frame_grad = np.diff(frame_mean)/255

############################# Find gradient thresholds 
fig, ax1 = plt.subplots()

ax1.set_xlabel('x-direction [px]') #Image of channel
ax1.set_ylabel('y-dricetion [px]')
ax1.imshow(frame_bw,cmap='gray')

ax2 = ax1.twinx() #Intensities
ax2.set_ylabel('gradient [-1;1]')
ax2.plot(np.arange(0, len(frame_grad)), frame_grad, color='r')

#ax3 = ax1.twinx() #Intensities
ax3 = ax2.twiny()
ax3.axis('off')
thresh_line, = ax3.plot(np.arange(0, len(frame_grad)), np.array([0]*len(frame_grad)), color='b')

# Make a horizontal slider to control the frequency.
axthresh = fig.add_axes([0.2, 0.01, 0.65, 0.01])
thresh_slider = Slider(ax=axthresh, label='Threshold', valmin=np.min(frame_grad)*1.1, valmax=np.max(frame_grad)*1.1, valinit=0)

# The function to be called anytime a slider's value changes
def update(val):
    global slider_val
    slider_val = val
    thresh_line.set_ydata(np.array([val]*len(frame_grad)))
    fig.canvas.draw_idle()

# register the update function with each slider
thresh_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to accept the slider value.
min_val = fig.add_axes([0.0125, 0.05, 0.1, 0.04])
max_val = fig.add_axes([0.875, 0.05, 0.1, 0.04])
button_min = Button(min_val, 'Min', hovercolor='0.975')
button_max = Button(max_val, 'Max', hovercolor='0.975')
    
def assign_min(event): #A function that assigns the threshold value given by the slider
    global threshold_min
    threshold_min = globals()['slider_val']
    print('The min threshold has been set to: ' + str(round(threshold_min,3)))
    if 'threshold_max' in globals():
        plt.close(fig)

def assign_max(event): #A function that assigns the threshold value given by the slider
    global threshold_max
    threshold_max = globals()['slider_val']
    print('The max threshold has been set to: ' + str(round(threshold_max,3)))
    if 'threshold_min' in globals():
        plt.close(fig)

button_min.on_clicked(assign_min)
button_max.on_clicked(assign_max)

fig.tight_layout()
plt.show()


img_mid = int(np.round(len(frame_grad)/2)) #Midpoint of the image

index_left_side = np.array([])
index_right_side = np.array([])

for (i,j) in enumerate(frame_grad[0:img_mid]):
     if (j < threshold_min):
         index_left_side = np.append(index_left_side,[i])
         
for (i,j) in enumerate(frame_grad):
     if (j > threshold_max) and (i >= img_mid):
         index_right_side = np.append(index_right_side,[i])
 
index_left_side = int(np.max(index_left_side))
index_right_side = int(np.min(index_right_side))
px_per_mm = (index_right_side-index_left_side)/0.4 #px/mm
 
#%%
frame = frame[:, index_left_side: index_right_side]
frame_mean = frame_mean[index_left_side: index_right_side]
ave_frame_cut = np.round(np.tile(frame_mean, (len(frame_mean),1)))/255 #Cut frame avereaged along y-driection

cv2.namedWindow("Frame - Area of interest", cv2.WINDOW_NORMAL)
cv2.imshow("Frame - Area of interest", frame)     
 
