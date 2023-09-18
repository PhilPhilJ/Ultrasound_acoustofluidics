#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 12:12:46 2023

@author: joakimpihl
"""


import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button

def frameCut(frame):
    global index_left_side
    global index_right_side
    
    ######################################## Functions start ########################################
    # The function to be called anytime a slider's value changes
    def update(val):
        print(val)
        slider_val = val
        vert_line.set_xdata(val)
        fig.canvas.draw_idle()
        
    def assign_min(event): #A function that assigns the threshold value given by the slider
        global index_left_side
        global px_per_mm
        globals()['index_left_side'] = globals()['slider_val']
        print('The left boundary has been set at: ' + str(round(index_left_side,0)))
# =============================================================================
#         if 'index_right_side' in globals():
#             px_per_mm = (index_right_side-index_left_side)/0.4 #px/mm
#             print('For the view there is ' + str(round(px_per_mm,2)) + ' px/mm')
#             plt.close(fig)
# 
# =============================================================================
    def assign_max(event): #A function that assigns the threshold value given by the slider

        global px_per_mm
        globals()['index_right_side'] = globals()['slider_val']
        print('The right boundary has been set at: ' + str(round(index_right_side,0)))
# =============================================================================
#         if 'index_left_side' in globals():
#             px_per_mm = (index_right_side-index_left_side)/0.4 #px/mm
#             print('For the view there is ' + str(round(px_per_mm,2)) + ' px/mm')
#             plt.close(fig)
#     
# =============================================================================
    ######################################## Functions end ########################################
    funcStop = True
    frame_length = np.size(frame, axis=0)

    fig, ax1 = plt.subplots()
    fig.set_size_inches(20/2.54, 15/2.54)
    
    ax1.set_xlabel('x-direction [px]') #Image of channel
    ax1.set_ylabel('y-dricetion [px]')
    ax1.imshow(frame,cmap='gray')

    ax2 = ax1.twinx() #Intensities
    ax2.set_ylabel('Intensity [0;255]')
    ax2.plot(np.arange(0, frame_length), np.mean(frame, axis=0), color='r')

    ax3 = ax1.twinx() #Line determining left and right side of the channel
    ax3.axis('off')
    vert_line = plt.axvline(x=frame_length/2, color = 'b')

    # Make a horizontal slider to control the line position.
    axpos = fig.add_axes([0.2, 0.01, 0.65, 0.03])
    pos_slider = Slider(ax=axpos, label='Position', valmin=0, valmax=frame_length, valinit=frame_length/2)
    # register the update function with each slider
    #pos_slider.on_changed(update)

    # Create a `matplotlib.widgets.Button` to accept the slider value.
    min_val = fig.add_axes([0.0125, 0.05, 0.1, 0.04])
    max_val = fig.add_axes([0.875, 0.05, 0.1, 0.04])
    button_min = Button(min_val, 'Min', hovercolor='0.975')
    button_max = Button(max_val, 'Max', hovercolor='0.975')
    #button_min.on_clicked(assign_min)
    #button_max.on_clicked(assign_max)
    
    while not (('index_left_side' in globals()) and ('index_right_side' in globals())):
        # register the update function with each slider
        pos_slider.on_changed(update)

        # Create a `matplotlib.widgets.Button` to accept the slider value.
        button_min.on_clicked(assign_min)
        button_max.on_clicked(assign_max)
    

            
    plt.close(fig)
    
    return index_left_side, index_right_side, px_per_mm
     
#%%

#vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video
vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video


#Reads the fist frame
ret, frame = vid.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
#%%

frameCut(frame)
plt.show()