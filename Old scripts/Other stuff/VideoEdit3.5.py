#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:30:30 2023

@author: joakimpihl
"""

import cv2, os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
#%%
path = '/Users/joakimpihl/Desktop/Big sweep/'
path_out = '/Users/joakimpihl/Desktop/Big sweep cropped/'
#%%
input_path_0 = path + 'run 1Frequency 1.91Hz/frequency1.91.mp4'

vid = cv2.VideoCapture(input_path_0)

#Crop image data 
####################################### Define functions start #######################################
def update(val): # The function to be called anytime a slider's value changes
    global slider_val
    slider_val = val
    vert_line.set_xdata(val)
    fig.canvas.draw_idle()
    
def assign_min(event): #A function that assigns the threshold value given by the slider
    global index_left_side
    index_left_side = int(globals()['slider_val'])
    print('The min threshold has been set to: ' + str(round(index_left_side,0)))
    if 'index_right_side' in globals() and 'focus_point' in globals():
        plt.close(fig)

def assign_max(event): #A function that assigns the threshold value given by the slider
    global index_right_side
    index_right_side = int(globals()['slider_val'])
    print('The max threshold has been set to: ' + str(round(index_right_side,0)))
    if 'index_left_side' in globals() and 'focus_point' in globals():
        plt.close(fig)
        
def assign_mid(event): #A function that assigns the threshold value given by the slider
    global focus_point
    focus_point = int(globals()['slider_val'])
    print('The channel focuspoint has been set to: ' + str(round(focus_point,0)))
    if 'index_left_side' in globals() and 'index_right_side' in globals():
        plt.close(fig)
####################################### Define functions end #######################################

#Reads the fist frame
vid.set(cv2.CAP_PROP_POS_FRAMES, int(vid.get(cv2.CAP_PROP_FRAME_COUNT)*0.75))
ret, frame = vid.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
frame_length = np.size(frame, axis=1)

####################################### Plotting intensities overlayed image of channel #######################################
fig, ax1 = plt.subplots()
fig.set_size_inches(20/2.54, 15/2.54)

ax1.set_xlabel('x-direction [px]') #Image of channel
ax1.set_ylabel('y-dricetion [px]')
ax1.imshow(frame,cmap='gray')

ax2 = ax1.twinx() #Intensities
ax2.set_ylabel('Intensity [0;255]')
ax2.plot(np.arange(0, frame_length), np.mean(frame, axis=0), color='r')

#ax3 = ax1.twinx() #Intensities
ax3 = ax1.twinx()
ax3.axis('off')
vert_line = plt.axvline(x=frame_length/3, color = 'b')

# Make a horizontal slider to control the line position.
axpos = fig.add_axes([0.2, 0, 0.65, 0.03])
pos_slider = Slider(ax=axpos, label='Position', valmin=0, valmax=frame_length, valinit=frame_length/3)

# register the update function with each slider
pos_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to accept the slider value.
min_val = fig.add_axes([0.0125, 0.05, 0.1, 0.04])
max_val = fig.add_axes([0.875, 0.05, 0.1, 0.04])
mid_val = fig.add_axes([0.45, 0.9, 0.1, 0.04])
button_min = Button(min_val, 'Min', hovercolor='0.975')
button_max = Button(max_val, 'Max', hovercolor='0.975')
button_mid = Button(mid_val, 'Mid', hovercolor='0.975')

button_min.on_clicked(assign_min)
button_max.on_clicked(assign_max)
button_mid.on_clicked(assign_mid)

vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
#%%

# Paths to files
delta = 0
num = 0
for folder_path in os.listdir(path): #Video 0 through 10
    folder_path = os.path.join(path, folder_path)
    if folder_path =='/Users/joakimpihl/Desktop/Big sweep/.DS_Store':
        print('Hi')
    else:
        for filename in os.listdir(folder_path):
            if os.path.isfile(filename) and filename.startswith('.DS'):
                break
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.startswith('frequency'):
                input_path = file_path
            if os.path.isfile(file_path) and filename.startswith('Time'):
                path_times = file_path
                freq = pd.read_csv(path_times, delimiter=';', encoding='utf-8')['Frame time'].iloc[1].tolist()
            if os.path.isfile(file_path) and filename.startswith('Important'):
                path_imp_times = file_path
        
        output_path = path_out + 'run ' + str(num) + '.mp4'
        output_imp_times = path_out + 'run ' +str(num) + ' Important times.csv'
        output_times = path_out + 'run ' +str(num) + ' Time Stamps.csv'
        
        df_imp_times = pd.read_csv(path_imp_times, delimiter=';', encoding='utf-8')
        df_times = pd.read_csv(path_times, delimiter=';', encoding='utf-8')
        df_imp_times.to_csv(output_imp_times, sep=';', encoding='utf-8')
        df_times.to_csv(output_times, sep=';', encoding='utf-8')
        
        vid = cv2.VideoCapture(input_path)
          
        total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        FPS = vid.get(cv2.CAP_PROP_FPS)
        output_size = (int(index_right_side - index_left_side), height)
        
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Use 'H264' codec
        # Use 'MJPG' codec
        out = cv2.VideoWriter(output_path, fourcc, FPS, output_size)
    
        for i in range(total_frames):
            ret, frame = vid.read()
            if not ret:
                break
          
            # Convert to grayscale
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          
            # Crop the width
            frame_gray_cropped = frame_gray[:, index_left_side:index_right_side]
          
            # Convert to uint8
            frame_gray_cropped = frame_gray_cropped.astype(np.uint8)
          
            # Write the processed frame
            out.write(frame_gray_cropped)
            print(f"Processed frame {i}/{total_frames}")
        num += 1
        
        # Release resources
        vid.release()
        out.release()
        cv2.destroyAllWindows()

