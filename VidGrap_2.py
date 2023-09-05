#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:55:36 2023

@author: joakimpihl
"""

# Code for generating the first recording op particle focusing to be used for practice of image analysis

from pypylon import pylon
import serial, time
import cv2
import sys
sys.path.append('C:/Users/s102772/Desktop/Ultrasound_acoustofluidics/')
from AD_func import *
import numpy as np

print('Press ESC to close the window')

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

#cap = cv2.VideoCapture(0) #VideoCapture object which stores the frames, the argument is just the device index (may be 0, or -1)
size = (4504, 4504) # Camera resoloution: 4504x4504px, FPS: 18
FPS = 18 # Frames per second of camera
fourcc = cv2.VideoWriter_fourcc(*'mp4v') #Defines output format, mp4
out = cv2.VideoWriter('C:/Users/s102772/Desktop/Algae_Vid_7.mp4', fourcc, FPS, size) #Change path to saved location

#Connect to analog discovery
Connect()
t = 1


while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    record = -1
    
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
        cv2.imshow('Algae experiment', img)
        k = cv2.waitKey(1)
        if k == ord('r'): # press down r to record
            record = True
            print('Starting recording..')
        elif k == ord('s'): #Stop recording
            record = False    
            print('Stopping recording..')
        if record:
            out.write(img)
        if k == ord('f'): # press f
            funcGen()
        if k == ord('p'): # press F
            funcGen(freq=3.82)
        if k == ord('g'): # press g
            funcStop()
            
################################### Deletes unwanted data
        #average the video along y-dricetion so that we get an 1D array/vector
        frame_1d = np.array(np.mean(img, axis=0))
        
        if t == 1:
            grad = abs(np.diff(frame_1d))
            
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
            
        frame = frame[index_left_side: index_right_side]
        frame_1d = frame_1d[index_left_side: index_right_side]
            
        ave_frame_cut = np.round(np.tile(frame_1d, (len(frame_1d),1)))/255 #Cut frame avereaged along y-driection
            
        cv2.namedWindow("Frame - Area of interest", cv2.WINDOW_NORMAL)
        cv2.imshow("Frame - Area of interest", ave_frame_cut)     

###########################################         
            
            
            
            
            
            
            
            
            
            
            
# Close experiment
        if k == 27: # press ESC
            cv2.destroyAllWindows()
            disconnect()
            break

    t+=1
    grabResult.Release()

    
# Releasing the resource   
out.release() 
camera.StopGrabbing()

