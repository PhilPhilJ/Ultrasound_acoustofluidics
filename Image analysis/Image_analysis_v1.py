#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 13:40:02 2023

@author: joakimpihl
"""

import cv2
import numpy as np

################################# This part is only for loading a premade video #################################
#vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video
vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video


#Reads the fist frame
ret, frame = vid.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
frame = frame[:,1044:3025]
#################################################################################################################

frame_mean_y = np.mean(frame, axis=0) #Finds the mean along vertical/y-axis

#Defines the section which makes up the image
section_indeces = np.array([0, np.ceil(len(frame_mean_y)*0.47), np.floor(len(frame_mean_y)*0.53), len(frame_mean_y)], dtype=int)


section_1 = frame_mean_y[section_indeces[0]: section_indeces[1]]
section_2 = frame_mean_y[section_indeces[1]: section_indeces[2]]
section_3 = frame_mean_y[section_indeces[2]: section_indeces[3]]

#Find mean intensities
intensity_mean = np.mean(frame_mean_y)
intensity_sd = np.std(frame_mean_y)

#Mean intensity in section 1 and 3 (Here lies an assumption that the particle behavior is symmetric around the mid-point)
intensity_s1s3_mean = (np.mean(frame_mean_y[section_indeces[0]: section_indeces[1]])+np.mean(frame_mean_y[section_indeces[2]: section_indeces[3]]))/2 
intensity_s2_mean = np.mean(frame_mean_y[section_indeces[1]: section_indeces[2]]) # Mean intensity of section 2

