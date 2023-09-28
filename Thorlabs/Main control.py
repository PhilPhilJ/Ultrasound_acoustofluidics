# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:41:26 2023

@author: Phili
"""



###############################################################################
### For controlling lab setup.

import numpy as np
from pypylon import pylon
import cv2
import sys
sys.path.append(r'C:\Users\s102772\Desktop\Ultrasound_acoustofluidics\Thorlabs')
from ThorlabsFunctions import *
import time
from AD_func import *
#from freqSweep import *

#%%
###############################################################################
### Move to position

## Change this to skib if already homed
Homed = True

if Homed == False:
    print("Homing...")

    HomeX()
    HomeAll()

print("The device is homed in all directions")

### Input the starting position (bottom position of the tube) and top position. Make sure the device has not been moved since
### last use.

coordinate_bottom =  [45.044275, 26.14545, 27.02866]
coordinate_top =  [44.797575, 26.19676, 48.31306]

tube_length = coordinate_top[2] - coordinate_bottom[2]
print("coordinate_bottom is " + str(coordinate_bottom) + ", coordinate_top is " + str(coordinate_top) + " and the tube length is " + str(tube_length))

print("It is important that the GCTH has not been moved since last use because the camara could move in to the holder. The coodinate is set to: "+ str(coordinate_bottom))
user_input = input('Would you like to continue (y/n)')

if user_input.lower() == 'y':
    print('user typed "y" and the program will continue')
elif user_input.lower() == 'n':
    sys.exit('user typed "n" and the program will terminate now')
else:
    print('Type "y" or "n"')
    
##Change this to skib if in starting position
in_start_pos = True

if in_start_pos == False:
    print("moving to starting position")
    MoveRelY(coordinate_bottom[1])
    MoveRelZ(coordinate_bottom[2])
    MoveRelX(coordinate_bottom[0])

print("The device is now in the starting position")

#%%
###############################################################################
### Doing analysis of capillary tube

## Initialize camara


#Connect to analog discovery
Connect()

#number of runs for characterization of tube. note that the tube length is given and one frame is 0.84 mm therefore the number 
#should be tube_length/frame_height but could be more.
move_length = 0.84
runs = np.ceil(tube_length / move_length)
run_count = 1

#frequency for focusing
frequency = 3.82 

#voltages for the tone generator
volts = [1, 10, 20]

#start and stop frequencies for sweep
sweep = [3, 5]


print("Characterization of tube is about to begin and will run for ")
user_input = input('Would you like to continue (y/n)')

if user_input.lower() == 'y':
    print('user typed "y" and the program will continue')
elif user_input.lower() == 'n':
    sys.exit('user typed "n" and the program will terminate now')
else:
    print('Type "y" or "n"')
    
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

#the current position of the camera
position = coordinate_bottom

#path for file to be saved
path = "C:/Users/s102772/Desktop/" + "P[" + str(position[0]) + "," + str(position[1]) + "," + str(position[2]) + "]F[" + str(frequency) + "]V[" + str(volts[0]) + "," + str(volts[1]) + "," + str(volts[2]) + "]S[" + str(sweep[0]) + "," + str(sweep[1]) + "].mp4"

out = cv2.VideoWriter('C:/Users/s102772/Desktop/Algae_Vid_Exp.mp4', fourcc, 18, size) #Change path to saved location

#counter for while loop
count = 0

#messuring the time
current_time = time.time()

#creating statements
background = True
first = True
doing_volts = False
doing_sweeps = False

#wait times
wait_time = 2.5


while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    record = True
    
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
        cv2.imshow('Algae experiment', img)
        
        #position = [PositionX(), PositionY(), PositionZ()]

### starting the recording
        

        if record == True:
            out.write(img)
        
        if background == True:
            
            new_time = time.time()
            
            if first == True:
                print("making a background image over " +str(wait_time) + " s")
                first = False
            
            if current_time + wait_time < new_time:
                
                print("making background done")
                background = False
                doing_volts = True
                first = True
                
### focusing at different amplitudes
 

        if doing_volts == True:
        
            new_time = time.time()
            
            if first == True:
                print("Now focusing...")
                funcGen(freq=frequency, Amplitude=volts[count])
                first = False
            
            if current_time + wait_time < new_time:
                
                print("Focusing at freguency: " + str(frequency) + " Hz and amplitude: " + str(volts[count]) + " V")
                count = count + 1
                first = True
                
                if count >= len(volts):
                    
                    doing_volts = False
                    doing_sweeps = True

### doing sweeps in frequencies
        
        
        if doing_sweeps == True:
        
            new_time = time.time()
            
            if first == True:
                print("Now sweeping...")
                freqSweep(start=sweep[0],stop=sweep[1])
                first = False
            
            if current_time + wait_time < new_time:
                
                print("Freguency sweep from : " + str(sweep[0]) + " Hz to: " + str(sweep[1]) + " Hz")
                doing_sweeps = False
                record == False
                first == True
                
### moving to next position
        

        if record == False:
            
            if first == True:
                print("Now moving to next position...")
                MoveAbsZ(move_length)
                first = False
                
            moving_position = PositionZ()
            
            if moving_position == position[2] + move_length:
                position[2] = position[2] + moving_position
                print("Now in next position")
                run_count = run_count + 1
                
                if run_count == runs:
                    # Close experiment
                    cv2.destroyAllWindows()
                    disconnect()
                    break

    grabResult.Release()


