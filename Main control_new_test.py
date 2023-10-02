# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 09:45:48 2023

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
Homed = False

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
run_count = runs

#frequency for focusing
frequency = 3.82 

#voltages for the tone generator
volts = [1, 10, 20]

#start and stop frequencies for sweep
sweep = [3, 5]

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
wait_time = 1

#creating statements
background = True
first = True
doing_volts = False
doing_sweeps = False
move = False

position = [PositionX(), PositionY(), PositionZ()]

while run_count > 0:
    #messuring the time
    current_time = time.time()
    
    ### Making background
    
    while background == True:
        
        new_time = time.time()
        
        if first == True:
            print("making a background image over " +str(wait_time) + " s")
            first = False
        
        if current_time + wait_time < new_time:
            
            print("making a background done")
            background = False
            doing_volts = True
            first = True
            current_time = time.time()
            
    ### focusing at different amplitudes
     
    
    while doing_volts == True:
    
        new_time = time.time()
        
        if first == True:
            print("Now focusing...")
            funcGen(freq=frequency, Amplitude=volts[count])
            first = False
        
        if current_time + wait_time < new_time:
            
            print("Focusing at freguency: " + str(frequency) + " Hz and amplitude: " + str(volts[count]) + " V")
            first = True
            doing_sweeps = True
            count += 1
            current_time = time.time()
            
            if count == len(volts):
                
                doing_volts = False
                count = 0

    
    ### doing sweeps in frequencies
    
    
    #this part is not done yet and only does a print-statement
    while doing_sweeps == True:
    
        new_time = time.time()
        
        if first == True:
            print("Now sweeping...")
            #freqSweep(start=sweep[0],stop=sweep[1])
            first = False
            current_time = time.time()
        
        if current_time + wait_time < new_time:
            
            print("Freguency sweep from: " + str(sweep[0]) + " Hz to: " + str(sweep[1]) + " Hz with: " + str(volts[count]) + " V")

            first = True
            count += 1
            current_time = time.time()
            
            
            if count == 3:#change tihs to len(volt)
                
                doing_sweeps = False
                move = True
                count = 0

            
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
            run_count -= 1
            
            #creating statements
            background = True
            first = True
            doing_volts = False
            doing_sweeps = False
            move = False
            
            print("there are " + str(run_count) + " left out of a total of " + str(runs))
            
print("characterization of tube is done")