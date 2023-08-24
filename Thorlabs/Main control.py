# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:41:26 2023

@author: Phili
"""


from pypylon import pylon
import cv2
import sys
sys.path.append('C:/Users/s102772/Desktop/Algae_Python')
from AD_func import *
import time

###############################################################################
### For controlling lab setup.

from ThorlabsFunctions import *
import numpy as np
from pypylon import pylon
import cv2
import sys
sys.path.append('C:/Users/s102772/Desktop/Algae_Python')
from AD_func import *

###############################################################################
### Move to position

## Set homed
Homed = False

if homed == True:

    HomeX()
    HomeY()
    HomeZ()

print("The device is homed in all directions")

### Input the starting position. Make sure the device hs not been moved since
### last use.

coordinate =  [30, 20, 5]

MoveRelX(coordinate[0])
MoveRelY(coordinate[1])
MoveRelZ(coordinate[2])

start_coordinate = [PositionX(), PositionY(), PositionZ()]

print("The device is now in the starting position")

###############################################################################
### Doing analysis of capillary tube

## Initialize camara

# Move in position for analysis
print('Press ESC to close the window')

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

size = (4504, 4504) # Camera resoloution: 4504x4504px, FPS: 18
fourcc = cv2.VideoWriter_fourcc(*'mp4v') #Defines output format, mp4
out = cv2.VideoWriter('C:/Users/s102772/Desktop/Algae_Vid_7.mp4', fourcc, 18, size) #Change path to saved location

#Connect to analog discovery
Connect()

initialize_analysis = False
firsttime = True

# Set the amount of time to analyse algae focusing
t_end = time.time() + 10

while camera.IsGrabbing():
    
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    # Access the image data
    image = converter.Convert(grabResult)
    img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
    cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
    cv2.imshow('Algae experiment', img)
    
    ## Determining the length of the tube
    
    img_mean_x = np.mean(img, axis = 1)
    difference_x = img_mean_x[0] - img_mean_x[-1]
    
    if difference_x > 0:
        MoveAbsZ(2)
        
    if difference_x < 0:   
        
        end_z = PositionZ()
        tube_length = abs(start_coordinate[2] - end_z)
        initialize_analysis = True
    
    if initialize_analysis == True:
        
        if firsttime == True:
            
            MoveRelZ(-1)
            HomeZ()
            MoveRelZ(start_coordinate[2])
            firsttime = False
        
        MoveAbsZ(3)
        funcGen()
        
        while time.time() < t_end:
            out.write(img)
        
        funcStop()
        current_position = PositionX()
        
    if current_position > end_z:
        
        cv2.destroyAllWindows()
        disconnect()
        break


    grabResult.Release()

    
# Releasing the resource   
out.release() 
camera.StopGrabbing()


###############################################################################
###############################################################################
### Check the tilt of the device

## Initialize camara


 ## Something camara / focus
 end_coordinate = [PositionX(), PositionY(), PositionZ()]

 # Calculating the angle tilt
 tilt = end_coordinate[2] - start_coordinate[2] / end_coordinate[1] - start_coordinate[1]
 angle = np.arctan(tilt)

 print("The tilt angle is " +str(angle))

 # Move to start

 MoveAbsX(start_coordinate[0], start_coordinate[1], start_coordinate[2])

 print("The tilt check is done and the device is back in starting position")
###############################################################################


