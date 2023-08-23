# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:41:26 2023

@author: Phili
"""

###############################################################################
### For controlling labb setup.

from ThorlabsFunctions import *
import numpy as np

###############################################################################
### Move to position

CheckHomeX()
if homed == False:
    HomeX()

CheckHomeY()
if homed == False:
    HomeY()

CheckHomeX()
if homed == False:
    HomeY()

print("The device is homed in all directions")

### Input the starting position. Make sure the device hs not been moved since
### last use.

coordinate =  [x , y, z]

MoveRelX(coordinate[0])
MoveRelY(coordinate[1])
MoveRelZ(coordinate[2])

start_coordinate = [PositionX(), PositionY(), PositionZ()]

print("The device is now in the starting position")

###############################################################################
### Check the tilt of the device

## Initialize camara

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


