#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 13:40:02 2023

@author: joakimpihl
"""

import cv2
import numpy as np
import time

################################# This part is only for loading a premade video #################################
#vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video
vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video


while True:
    #Reads the fist frame
    ret, frame = vid.read()
    if ret != True:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    frame = frame[:,1044:3025]
    #################################################################################################################
    
    frame_mean_y = np.mean(frame, axis=0) #Finds the mean along vertical/y-axis
    frame_background_y = np.zeros(len(frame_mean_y)) #Should be replaced by a background image
    frame_mean_y = frame_mean_y-frame_background_y #Subtract background
    
    
    #Defines the section which makes up the image
    section_indeces = np.array([0, np.ceil(len(frame_mean_y)*0.47), np.floor(len(frame_mean_y)*0.53), len(frame_mean_y)], dtype=int)
    
    #Find sd  on intensities
    intensity_sd = np.std(frame_mean_y)
    
    #Mean intensity in section 1 and 3 (Here lies an assumption that the particle behavior is symmetric around the mid-point)
    intensity_s2_mean = np.mean(frame_mean_y[section_indeces[1]: section_indeces[2]]) # Mean intensity of section 2
    
    #Has a frame been passed already
    no_diff = 0
    mm_px = 0.20010005002501252 # um/px
    dist = int(np.ceil(section_indeces[1:2]) - np.floor(np.mean(section_indeces[0:1]))) * mm_px
    print(no_diff)
    
    if 'frame_mean_init' in globals():
        frame_diff = frame_mean_y-frame_mean_init
        frame_mean_init = frame_mean_y
        
        diff_section = abs(np.mean(frame_diff[section_indeces[1]:section_indeces[2]]))
                                                                                    
        if (diff_section <= intensity_sd) and (no_diff < 1):
            no_diff += 1
        elif (diff_section <= intensity_sd) and (no_diff >= 1):
            stop = time.time()
            focus_time = stop-start - no_diff/18
            speed = dist/focus_time
            print(focus_time)
            print(speed)
        
    else:
        frame_mean_init = np.copy(frame_mean_y)
        start = time.time()
        