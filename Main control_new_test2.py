# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:12:37 2023

@author: Phili
"""

###############################################################################
### For controlling lab setup.

import numpy as np
from pypylon import pylon
import cv2
import sys
sys.path.append(r'C:\Users\s102772\Desktop\Ultrasound_acoustofluidics')
from ThorlabsFunctions import *
import time
from AD_func import *
from freqSweep import *

#%%
###############################################################################
### Move to position

## Set homed
Homed = True
in_position = True

if Homed == False:
    print("Homing...")

    HomeX()
    HomeAll()

print("The device is homed in all directions")

### Input the starting position (bottom position of the tube) and top position. Make sure the device has not been moved since
### last use.

coordinate_bottom =  [43.04160, 26.24083, 28.9598]
coordinate_top =  [43.04160, 26.24083, 43.62598]

tube_length = coordinate_top[2] - coordinate_bottom[2]
print("coordinate_bottom is " + str(coordinate_bottom) + "and coordinate_top is " + str(coordinate_top) + " and the tube length is " + str(tube_length))

print("It is important that the GCTH has not been moved since last use because the camara could move in to the holder. The coodinate is set to: "+ str(coordinate_bottom))
user_input = input('Would you like to continue (y/n)')

if user_input.lower() == 'y':
    print('user typed "y" and the program will continue')
elif user_input.lower() == 'n':
    sys.exit('user typed "n" and the program will terminate now')
else:
    print('Type "y" or "n"')

if in_position == False:
    print("moving to starting position")
    MoveRelY(coordinate_bottom[1])
    MoveRelZ(coordinate_bottom[2])
    MoveRelX(coordinate_bottom[0])

print("The device is now in the starting position")

#%%
###############################################################################
### Doing analysis of capillary tube

## setting up folder for videos
newpath = r'C:\Users\Phili\OneDrive\Skrivebord' #change path to save location
first_folder_path = os.path.join(newpath, 'Algae experiment')
os.mkdir(new_folder_path)

## Initialize camara

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
FPS = 7.4 # Frames per second of camera
fourcc = cv2.VideoWriter_fourcc(*'mp4v') #Defines output format, mp4
out = cv2.VideoWriter(os.path.join(first_folder_path, roc_name), fourcc, FPS, size) #Change path to saved location

record = -False

#Connect to analog discovery
Connect()

#number of runs for characterization of tube. note that the tube length is given and one frame is 0.84 mm therefore the number 
#should be tube_length/frame_height but could be more.
move_length = 0.84
runs = np.ceil(tube_length / move_length)
run_count = 0

#frequency for focusing
frequency = 3.82 

#voltages for the tone generator
volts = [1, 10, 20]

#start and stop frequencies for sweep
sweep_int = [frequency - 0.1, frequency + 0.1]
step = 5
sweep = np.linspace(sweep_int[0], sweep_int[1], step)
sweeper = 0
frequency = sweep[sweeper]


#Connect to analog discovery
Connect()

print("Characterization of tube is about to begin and will run for ")
user_input = input('Would you like to continue (y/n)')

if user_input.lower() == 'y':
    print('user typed "y" and the program will continue')
elif user_input.lower() == 'n':
    sys.exit('user typed "n" and the program will terminate now')
else:
    print('Type "y" or "n"')
    

#the current position of the camera
position = coordinate_bottom

#counter for while loop
count = 0

#wait times
wait_time = 10

#creating statements
background = True
first = True
focus = False
move = False

position = [PositionX(), PositionY(), PositionZ()]

while run_count != runs:
    
    ## creating the folder for this nun
    second_folder_path = os.path.join(new_folder_path,  str(run_count + 1) + ". run")
    os.mkdir(new_folder_path)
    
    #messuring the time
    current_time = time.time()
    
    ### Making background
    
    
    roc_name = "\backgroung_" + str(run_count + 1)
    record = True
    while camera.IsGrabbing() and background:
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
            #cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            out.write(img)
            
            new_time = time.time()
            
            if first == True:
                print("making a background image over " +str(wait_time) + " s")
                print(str(new_time-current_time) + "*")
                first = False
            
            if current_time + wait_time < new_time:
                
                print("making a background done")
                background = False
                focus = True
                first = True
                record = False
                
                current_time = time.time()
            
            if record == False:
                break
                
            grabResult.Release()

    # Releasing the resource   
    out.release() 
    camera.StopGrabbing()

            
    ### focusing at different amplitudes and frequencies
     
    roc_name = "\focus" + str(run_count + 1)
    while camera.IsGrabbing() and focus:
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
            #cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            out.write(img)
            
            new_time = time.time()
            
            if first == True:
                print("Now focusing...")
                funcGen(freq=frequency, Amplitude=volts[count])
                first = False
            
            if current_time + wait_time < new_time:
                
                print("Focusing at freguency: " + str(frequency) + " Hz and amplitude: " + str(volts[count]) + " V")
                first = True
                count += 1
                current_time = time.time()
                
                if count == len(volts):
                    
                    count = 0
                    sweeper += 1
                    
                    if sweeper == len(sweep):
                        focus = False
            
            if record == False:
                break
                
            grabResult.Release()

    # Releasing the resource   
    out.release() 
    camera.StopGrabbing()
    
            
    ### moving to next position
    
    while move == True:
        
        if first == True:
            print("Now moving to next position...")
            MoveRelZ(move_length)
            current_time = time.time()
            first = False
            
        
        new_time = time.time()
          
    
        if current_time + wait_time < new_time:
            position[2] = PositionZ()
            print("Now in next position")
            run_count += 1
            
            #creating statements
            background = True
            first = True
            focus = False

            move = False
            
            print(str(run_count) + ".  out of a total of " + str(runs))


file = open('output.txt', 'w')
file.write('Here is some data')
file.close()
print("characterization of tube is done")