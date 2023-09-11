# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:41:26 2023

@author: Phili
"""



###############################################################################
### For controlling lab setup.

from ThorlabsFunctions import *
import numpy as np
from pypylon import pylon
import cv2
import sys
sys.path.append('C:/Users/s102772/Desktop/Algae_Python')
from AD_func import *
import time

###############################################################################
### Move to position

## Set homed
Homed = False

if Homed == True:

    HomeAll()

print("The device is homed in all directions")

### Input the starting position. Make sure the device hs not been moved since
### last use.

coordinate =  [30, 20, 5]

print("It is important that the GCTH has not been moved since last use because the camara could move in to the holder. The coodinate is set to:")
print(coordinate)
user_input = input('Would you like to continue (y/n)')

if user_input.lower() == 'y':
    print('user typed "y" and the program will continue')
elif user_input.lower() == 'n':
    sys.exit('user typed "n" and the program will terminate now')
else:
    print('Type "y" or "n"')

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
    
    done = False
    while done == False:
        img_mean_y = np.mean(img, axis = 1)
        gradient_y = abs(np.diff(img_mean_y))
        
        if np.max(gradient_y) > 0.5:
            MoveAbsZ(2)
            
        else:   
            bottom_z = PositionZ()
            done = True
    
    done = False
    while done == False:
        img_mean_y = np.mean(img, axis = 1)
        gradient_y = abs(np.diff(img_mean_y))
        
        if np.max(gradient_y) < 0.5:
            MoveAbsZ(2)
            
        else:   
            top_z = PositionZ()
            done = True
    
    tube_length = top_z - bottom_z
    runs = 10
    
    
    initialize_analysis = True    
    if initialize_analysis == True:
        
        MoveAbsX(-1)
        MoveAbsZ(-1)
        MoveAbsZ(bottom_z)
        MoveAbsX(start_coordinate[0])
        
        for run in range(runs):
            funcGen()
            time.sleep(5)
            funcStop()
            
            MoveRelZ(tube_length / runs)
        
        
    if current_position >= top_z:
        
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


