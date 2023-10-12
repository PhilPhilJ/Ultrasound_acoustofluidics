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
#from frameCut import *
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
FPS = 18.0 # Frames per second of camera
fourcc = cv2.VideoWriter_fourcc(*'MP4V') #Defines output format, mp4
out = cv2.VideoWriter('C:/Users/s102772/Desktop/Algae_Vid_Exp.mp4', fourcc, FPS, size, False) #Change path to saved location

#Connect to analog discovery
Connect()
#t = 1
#test = 0
record = False
start = time.time()
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
 #   test += 1
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
# =============================================================================
#         if t==42:
#             img = img[:,IL:IR]
# =============================================================================
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
# =============================================================================
#         if t == 5:
#             IL,IR = frameCut(img)
#         if t<6:
#             t+=1
#         elif t!=42:
#             t=42
# =============================================================================
###########################################         
                     
# Close experiment
        if k == 27: # press ESC
            cv2.destroyAllWindows()
            disconnect()
            break
# =============================================================================
#         stop = time.time()
#         if (stop-start >= 10):
#             print('Delta_T: ' + str(stop-start))
#             print('expected loops = 10s * 18FPS = 180frames')
#             print('Loops: ' + str(test))
# =============================================================================
    grabResult.Release()

    
# Releasing the resource   
out.release() 
camera.StopGrabbing()

