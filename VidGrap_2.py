#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:55:36 2023

@author: joakimpihl
"""

# Code for generating the first recording op particle focusing to be used for practice of image analysis

from pypylon import pylon
import serial, time
import cv2
import sys
sys.path.append('C:/Users/s102772/Desktop/Ultrasound_acoustofluidics')
from AD_func import *
#from frameCut import *
import numpy as np
import pandas as pd
import os
from Valve_control import switchvalve

print('Press ESC to close the window')

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
#camera.AcquisitionFrameRate.SetValue(100);
#camera.AcquisitionFrameRateEnable.SetValue(True); 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

newpath = r"C:/Users/s102772/OneDrive - Danmarks Tekniske Universitet/Bachelorprojekt/Videoer/test of contrast and 2x focus"
if not os.path.exists(newpath):
    os.makedirs(newpath)

run = 13
frequencies = np.linspace(1.884, 1.906, 31 )
frequency = 1.884#frequencies[run]

#cap = cv2.VideoCapture(0) #VideoCapture object which stores the frames, the argument is just the device index (may be 0, or -1)
size = (1440, 1080) # Camera resoloution: 4504x4504px, FPS: 18
FPS = 20 # Frames per second of camera
fourcc = cv2.VideoWriter_fourcc(*"mp4v") #Defines output format, mp4
out = cv2.VideoWriter(newpath +"/run" + str(run) +'.mp4', fourcc, FPS, size, False) #Change path to saved location

##other parameters
temp = "24 C"
humid = "19%"
gain = "10 dB"
lamp = "10 V and 3.5 A"
Alg_gen = '2.3'
volts = np.linspace(0.1,2,20)
Voltage = 1.1#volts[run]
the_time = time.time()

file = open(newpath + "/info" + str(run) +'.txt', 'w')
file.write("Temperature =" + str(temp) + ", humidity =" + str(humid) + ", Gain =" + str(gain) + ", Light =" + str(lamp) + ', Algae generation = ' + str(Alg_gen) + ". The starting time is: " + str(the_time) + ". The voltage is: " +str(Voltage) + ". Frequency = " +str(frequencies[run]))
file.close()

frame_time = np.empty([1])

#Connect to analog discovery
Connect()
#t = 1.
#test = 0
imp_times = np.empty(1) #[0] = focus start, [1] = focus stop

record = False
start = time.time()
f_start = False
stopping = False
first = True
stop = False
record_starting_time = time.time()
new_time = time.time()
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
 #   test += 1
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
# =============================================================================
#         if t==42:
#             img = img[:,IL:IR]
# =============================================================================
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
        cv2.imshow('Algae experiment', img)
        k = cv2.waitKey(1)
        
        if k ==ord("q"):
            frequency = 3.78
        
        if k == ord('i'): # press down i to switch valve position
            switchvalve()
        
        if k == ord('r'): # press down r to record
            record = True
            frame_time = np.append(frame_time, frequency)
            record_starting_time = time.time()
            print('Starting recording..')
        elif k == ord('s'): #Stop recording
            
            record_starting_time = time.time()
            f_start = False
            stopping = True
            imp_times = np.append(imp_times, new_time)
        if stopping == True:
            
            new_time = time.time()
            if first == True:
                
                print('Stopping recording..')
                funcStop()
                first = False
                stop = True
        
        if record_starting_time+5<new_time and not f_start:
            record = False
        if record_starting_time+6<new_time and not f_start:
        
            cv2.destroyAllWindows()
            disconnect()
            the_time = time.time()
            df = pd.DataFrame({'Frame time':frame_time})
            df2 = pd.DataFrame({'Important times':imp_times})
            df.to_csv(newpath + "/Time Stamps" + str(run) +'.csv', sep=';', encoding='utf-8')
            df2.to_csv(newpath + "/Important times" + str(run) +'.csv', sep=';', encoding='utf-8')
            file = open(newpath + "/info" + str(run) +'.txt', 'a')
            file.write("The end time is: " + str(the_time))
            file.close()
            break
            
            
        if record:
            
            new_time = time.time()
            
            out.write(img)
            frame_time = np.append(frame_time, time.time())
            
            if record_starting_time+5<new_time and not f_start:
                f_start = True
                imp_times = np.append(imp_times, new_time)
                funcGen(freq=frequency, Amplitude=Voltage)
            
            
                
        if k == ord('f'): # press f
            funcGen(freq=frequency, Amplitude=Voltage)
        if k == ord('p'): # press F
            funcGen(freq=3.82, Amplitude=5)
        if k == ord('g'): # press g
            funcStop()
        if k == ord('w'): # press w 
            
            freqSweep(shape=funcSine,start=1.89,stop=1.93,by=2,Amplitude=1,v_Offset=0)
            
################################### Deletes unwanted data
# =============================================================================
#         if t == 5:
#             IL,IR = frameCut(img)
#         if t<6:
#             t+=1
#         elif t!=42:s
#             t=42
# =============================================================================
###########################################         
                     
# Close experiment
        if k == 27: # press ESC
            cv2.destroyAllWindows()
            disconnect()
            the_time = time.time()
            df = pd.DataFrame({'Frame time':frame_time})
            df2 = pd.DataFrame({'Important times':imp_times})
            df.to_csv(newpath + "/Time Stamps" + str(run) +'.csv', sep=';', encoding='utf-8')
            df2.to_csv(newpath + "/Important times" + str(run) +'.csv', sep=';', encoding='utf-8')
            file = open(newpath + "/info" + str(run) +'.txt', 'a')
            file.write("The end time is: " + str(the_time))
            file.close()
            break
# =============================================================================
#         stop = time.time()
#         if (stop-start >= 10):
#             print('Delta_T: ' + str(stop-start))
#             print('expected loops = 10s * 18FPS = 180frames')
#             print('Loops: ' + str(test))
# =============================================================================
    grabResult.Release()

    
# Releasing the resource   
out.release() 
camera.StopGrabbing()
funcStop()
