#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:54:06 2023

@author: joakimpihl
"""

from pypylon import pylon
import serial, time
import cv2
from AD_func import *

print('Press ESC to close the window')

arduinoSer = serial.Serial('COM3',baudrate=9600,timeout=0.5)
flow_on = 0;

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)
        k = cv2.waitKey(1)

        if k == 27: # press ESC
            cv2.destroyAllWindows()
            break
        #if k == 32: # press spacebar  
        #    if flow_on==0:
        #        arduinoSer.write(b'1')
        #        flow_on = 1
        #    else:
        #        arduinoSer.write(b'0')
        #        flow_on = 0
        #if k == 97: # press a (alive)
        #    arduinoSer.write(b'3') # on
        #if k == 100: # press d (dead) 
        #    arduinoSer.write(b'2') # off
            
        # Code for frequency control #

        if k == 102: # press f
            funcGen()
            
        if k == 70: # press f
            funcGen(freq=3.82)
            
        elif k == 103: # press g
            funcStop()
   
    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()

arduinoSer.write(b'0')

cv2.destroyAllWindows() 
arduinoSer.close()

