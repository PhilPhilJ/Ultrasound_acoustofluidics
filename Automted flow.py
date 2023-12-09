# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 14:46:25 2023

@author: s102772
"""

import cv2
from pypylon import pylon
import serial, time


print('Press ESC to close the window')

arduinoSer = serial.Serial('COM3',baudrate=9600,timeout=0.5)

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
static_time = time.time()
opengate = 0
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)
        k = cv2.waitKey(1)
        # print(k)
        
        current_time = time.time()
        
        if k == 27: # press ESC
            break
        if current_time > static_time + 10: 
                arduinoSer.write(b'1')
                static_time = time.time()
                print("I am here")
                opengate = 1
                
        if opengate == True and current_time > static_time+1: 
                arduinoSer.write(b'0')
                opengate = 0
                print("I am here now")
        
    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()

arduinoSer.write(b'0')

cv2.destroyAllWindows() 
arduinoSer.close()