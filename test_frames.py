#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:57:56 2023

@author: joakimpihl
"""

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

FPS = 18 # Frames per second of camera
record = -1
f = 0


while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
        cv2.imshow('Algae experiment', img)
        k = cv2.waitKey(1)
        
        
        if k == ord('l'):
            record = 10
            start = time.time()
        if record == 10:
            f += 1
        if f == 180:
            stop = time.time()
            break
        
                    
                     
# Close experiment
        if k == 27: # press ESC
            cv2.destroyAllWindows()
            break

    grabResult.Release()

    
# Releasing the resource   
camera.StopGrabbing()

print('times through the loop: ' + str(f))
print('time: ' + str(stop-start))

