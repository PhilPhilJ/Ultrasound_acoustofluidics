#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 11:13:41 2023

@author: joakimpihl
"""

from pypylon import pylon
import serial, time
import cv2

arduinoSer = serial.Serial('COM3',baudrate=9600,timeout=0.5)# - establishes link between Arduino and PC (Baudrate 9600 bits per second)
flow_on = 0; # Bolean var defines wether or not there's flow

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed #Opencv uses BGR colorformat instead of RGB i.e. the color order is: red, green, and blue
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) #Waits 5s for an img and then it retrieves it

    if grabResult.GrabSucceeded(): #Was the img grabbed succesfully?
        # Access the image data
        image = converter.Convert(grabResult) 
        img = image.GetArray() #Converts the image into an array which Opencv can process
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)#Names the display window
        cv2.imshow('title', img) #Displays the img
        k = cv2.waitKey(1)
        # print(k)
        if k == 27: # press ESC - Close the window
            break
        if k == 32: # press spacebar  
            if flow_on==0:
                arduinoSer.write(b'1')
                flow_on = 1
            else:
                arduinoSer.write(b'0')
                flow_on = 0
        if k == 97: # press a (alive)
            arduinoSer.write(b'3') # on
        if k == 100: # press d (dead) 
            arduinoSer.write(b'2') # off

  
        
    grabResult.Release()
    
