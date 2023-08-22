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
from AD_func import *

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
fourcc = cv2.VideoWriter_fourcc(*'MJPG') #Defines output format, mp4
out = cv2.VideoWriter('Algae_Vid.mp4', fourcc, 18.0, size)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
        cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
        cv2.imshow('Algae experiment', img)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        k = cv2.waitKey(1)
        
        if k == ord('r'): # press down r to record
            record = True
            if record:    
                out.write(img, gray)
                time.sleep(10)
                record = not record
        elif k == ord('f'): # press f
            funcGen()
        elif k == ord('F'): # press F
            funcGen(freq=3.82)
        elif k == ord('g'): # press g
            funcStop()
# Close experiment
        if k == 27: # press ESC
            cv2.destroyAllWindows()
            break

    grabResult.Release()

    
# Releasing the resource    
camera.StopGrabbing()
out.Release()
