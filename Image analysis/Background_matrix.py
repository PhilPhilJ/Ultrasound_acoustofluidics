#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 11:44:54 2023

@author: joakimpihl
"""

import cv2
import numpy as np
import pandas as pd

# =============================================================================
path_exp = '/Users/joakimpihl/Downloads/' #path to experiment folder




# =============================================================================
vid = cv2.VideoCapture('/Users/joakimpihl/Downloads/Algae_Vid_exp_1.mp4') #Loads the video
#Define boundaries found using Image_crop_v3.py

#Reads the fist frame
ret, frame = vid.read()
n_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
background = np.empty(np.size(frame, axis=1))

#Generate background
for i in range(n_frames):
    ret_2, back_frame = vid.read()
    back_frame = cv2.cvtColor(back_frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    back_frame_mean = np.mean(back_frame, axis=0)
    background = np.vstack([background, back_frame_mean])

mean_background = np.mean(background[1:np.size(background, axis=0)], axis=0)  







