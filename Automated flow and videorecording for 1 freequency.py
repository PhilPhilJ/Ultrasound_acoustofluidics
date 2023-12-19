# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:50:42 2023

@author: s102772
"""

import cv2
from pypylon import pylon
import serial, time
import os
import numpy as np
from AD_func import Connect, disconnect, funcStop
import pandas as pd


print('Press ESC to close the window')

arduinoSer = serial.Serial('COM3',baudrate=9600,timeout=0.5)

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

frequency = 1.884
newpath = r"C:/Users/s102772/OneDrive - Danmarks Tekniske Universitet/Bachelorprojekt/Videoer/Same frequency/Frequency " + str(frequency) + "Hz"
if not os.path.exists(newpath):
    os.makedirs(newpath)

#cap = cv2.VideoCapture(0) #VideoCapture object which stores the frames, the argument is just the device index (may be 0, or -1)
size = (1440, 1080) # Camera resoloution: 4504x4504px, FPS: 18
FPS = 20 # Frames per second of camera
fourcc = cv2.VideoWriter_fourcc(*"mp4v") #Defines output format, mp4
out = cv2.VideoWriter(newpath +"/frequency" + str(frequency) +'.mp4', fourcc, FPS, size, False) #Change path to saved location

##other parameters
temp = "24 C"
humid = "19%"
gain = "10 dB"
lamp = "10 V and 3.5 A"
Alg_gen = '2.3'
Voltage = 1
file = open(newpath + "/info" + str(frequency) +'.txt', 'w')
file.write("Temperature =" + str(temp) + ", humidity =" + str(humid) + ", Gain =" + str(gain) + ", Light =" + str(lamp) + ', Algae generation = ' + str(Alg_gen) + ". The voltage is: " +str(Voltage) + ". Frequency = " +str(frequency))
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

static_time = time.time()
opengate = 0
record = 1
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)
        k = cv2.waitKey(1)
        # print(k)
        
        current_time = time.time()
        
        if record == True:#recording is on
            frame_time = np.append(frame_time, frequency)
            record_starting_time = time.time()
            out.write(img)
            frame_time = np.append(frame_time, time.time())
            if first:
                print('Starting recording..')
                first = 0
        
        if k == 27: # press ESC
            break
        if current_time > static_time + 10 and not opengate: 
                arduinoSer.write(b'1')
                static_time = time.time()
                print("I am here")
                opengate = 1
                
        if opengate == True and current_time > static_time+10: 
                arduinoSer.write(b'0')
                opengate = 0
                print("I am here now")
                record = 0
                
        if not record:
         
                cv2.destroyAllWindows()
                the_time = time.time()
                df = pd.DataFrame({'Frame time':frame_time})
                df2 = pd.DataFrame({'Important times':imp_times})
                df.to_csv(newpath + "/Time Stamps" + str(frequency) + "Hz" +'.csv', sep=';', encoding='utf-8')
                df2.to_csv(newpath + "/Important times" + str(frequency) + "Hz" +'.csv', sep=';', encoding='utf-8')
                file.close()
                break
        
    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()
out.release() 

## Closing everything
disconnect()
arduinoSer.write(b'0')
arduinoSer.close()
funcStop()