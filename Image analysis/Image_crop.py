#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 13:08:18 2023

@author: joakimpihl
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

#vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Vid_For_Analysis.mp4') #Loads the video
vid = cv2.VideoCapture('/Users/joakimpihl/Downloads/Algae_Vid.mp4') #Loads the video


#Reads the fist frame
ret, frame = vid.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale

#average the video along y-dricetion so that we get an 1D array/vector
frame_1d = np.array(np.mean(frame, axis=0))
grad = abs(np.diff(frame_1d))

#ave_frame = np.round(np.tile(frame_1d, (len(frame_1d),1)))/255 #Frame avereaged along y-driection
#plt.plot(np.arange(0,len(frame_1d)-2), grad[0:4502])

grad[grad<=0.5] = 0
grad[grad>0.5] = 1

plt.plot(np.arange(0,len(frame_1d)-2), grad[0:4502])

img_mid = int(np.round(len(grad)/2)) #Midpoint of the image

index_left_side = np.array([])
index_right_side = np.array([])

for (i,j) in enumerate(np.diff(grad[0:img_mid])):
    if j < 0:
        index_left_side = np.append(index_left_side,[i])
        
for (i,j) in enumerate(np.diff(grad)):
    if (j > 0) and (i >= img_mid):
        index_right_side = np.append(index_right_side,[i])

index_left_side = int(np.max(index_left_side))
index_right_side = int(np.min(index_right_side))

frame = frame[:, index_left_side: index_right_side]
frame_1d = frame_1d[index_left_side: index_right_side]

ave_frame_cut = np.round(np.tile(frame_1d, (len(frame_1d),1)))/255 #Cut frame avereaged along y-driection

cv2.namedWindow("Frame - Area of interest", cv2.WINDOW_NORMAL)
cv2.imshow("Frame - Area of interest", ave_frame_cut)     

# =============================================================================
# 
# fourcc = cv2.VideoWriter_fourcc(*'mp4v') #Defines output format, mp4
# out = cv2.VideoWriter('/Users/joakimpihl/Desktop/TestVid.mp4', fourcc, 18, (index_right_side-index_left_side, 4054)) #Change path to saved location
# 
# while True:
#     #Reads the fist frame
#     ret, frame = vid.read()
#     frame = frame[:,index_left_side: index_right_side]
#     frame_1d = frame_1d[index_left_side: index_right_side]
# 
#     ave_frame_cut = np.round(np.tile(frame_1d, (len(frame_1d),1)))/255 #Cut frame avereaged along y-driection
#     out.write(ave_frame_cut)
#    
# =============================================================================
