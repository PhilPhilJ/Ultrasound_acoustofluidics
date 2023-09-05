#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 13:33:26 2023

@author: joakimpihl
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt



def frameCut(frame):
    #average the video along y-dricetion so that we get an 1D array/vector
    frame_1d = np.array(np.mean(frame, axis=0))
    grad = abs(np.diff(frame_1d))
    
    grad[grad<=0.5] = 0
    grad[grad>0.5] = 1
    
    img_mid = int(np.round(len(grad)/2)) #Midpoint of the image
    
    index_left_side = np.array([])
    index_right_side = np.array([])
    
    for (i,j) in enumerate(np.diff(grad[0:img_mid])):
        if j < 0:
            index_left_side = np.append(index_left_side,[i])
            
    for (i,j) in enumerate(np.diff(grad)):
        if (j > 0) and (i >= img_mid):
            index_right_side = np.append(index_right_side,[i])
    
    if (len(index_left_side)>0) and (len(index_right_side)>0):
        index_left_side = int(np.max(index_left_side))
        index_right_side = int(np.min(index_right_side))
        
        frame = frame[index_left_side: index_right_side]
        frame_1d = frame_1d[index_left_side: index_right_side]
        
        ave_frame_cut = np.round(np.tile(frame_1d, (len(frame_1d),1)))/255 #Cut frame avereaged along y-driection
    else:
        print('Error! Could not detect the channel edges')
    
    return index_left_side, index_right_side, ave_frame_cut
     