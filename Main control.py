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

###############################################################################
### For controlling labb setup.

from ThorlabsFunctions import *
import numpy as np
from pypylon import pylon
import cv2
import sys
sys.path.append('C:/Users/s102772/Desktop/Algae_Python')
from AD_func import *

###############################################################################
### Move to position

#HomeX()
#HomeY()
#HomeZ()

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
### Check the tilt of the device

## Initialize camara
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

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    record = -1
    
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
        cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
        cv2.imshow('Algae experiment', img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        k = cv2.waitKey(1)
        
        
        if k == ord('r'): # press down r to record
            record = True
            print('Starting recording..')
        elif k == ord('s'): #press s to stop recording
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
# Close experiment
        if k == 27: # press ESC
            cv2.destroyAllWindows()
            disconnect()
            break


    grabResult.Release()

    
# Releasing the resource   
out.release() 
camera.StopGrabbing()



# Moving Thorslab to top 



while dot == False:
    picture_hight = 1
    MoveAbsZ(picture_hight)
    
    ## Something camara / find dot
    if something:
        dot = True
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
### Doing analysis of capillary tube

## Initialize camara

# Move in position for analysis

###############################################################################


