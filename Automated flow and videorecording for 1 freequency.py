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
from AD_func import Connect, disconnect, funcStop, funcGen
import pandas as pd
from Valve_control import switchvalve


print('Press ESC to close the window')

arduinoSer = serial.Serial('COM3',baudrate=9600,timeout=0.5)
arduinoSer.write(b'0') # makes sure the flow is off

terminate = 0 #condition for breaking the for loop

#Connect to analog discovery
Connect()

frequencies = np.linspace(1.88, 1.91, 101)

for j in range(len(frequencies)):

    frequency = frequencies[j]    
    runs = 20
    for i in range(runs):
        # conecting to the first available camera
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        # Grabing Continusely (video) with minimal delay
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        converter = pylon.ImageFormatConverter()
        
        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    
        newpath = r"C:/Users/s102772/OneDrive - Danmarks Tekniske Universitet/Bachelorprojekt/Videoer/Same frequency/run" + str(i+1) + "Frequency " + str(frequency) + "Hz"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        #cap = cv2.VideoCapture(0) #VideoCapture object which stores the frames, the argument is just the device index (may be 0, or -1)
        size = (1440, 1080) # Camera resoloution: 4504x4504px, FPS: 18
        FPS = 20 # Frames per second of camera
        fourcc = cv2.VideoWriter_fourcc(*"mp4v") #Defines output format, mp4
        out = cv2.VideoWriter(newpath +
                              "/frequency" + str(frequency) +
                              '.mp4', fourcc, FPS, size, False) #Change path to saved location
        
        ##other parameters
        temp = "24 C"
        humid = "19%"
        gain = "10 dB"
        lamp = "10 V and 3.5 A"
        Alg_gen = '2.3'
        voltage = 1
        file = open(newpath + "/info" + str(frequency) +'.txt', 'w')
        file.write("Temperature =" + str(temp) + 
                   ", humidity =" + str(humid) + 
                   ", Gain =" + str(gain) + 
                   ", Light =" + str(lamp) + 
                   ", Algae generation = " + str(Alg_gen) + 
                   ". The voltage is: " +str(voltage) + 
                   ". Frequency = " +str(frequency)) #Writes the info file change parameters before a run
        file.close()
        
        #Create timestaps and points of focus stat/stop
        frame_time = np.empty([1])
        imp_times = np.empty(1) #[0] = focus start, [1] = focus stop
        
        #conditions used to control the if conditions
        first = True
        static_time = time.time()
        opengate = 0 # the "opengate" statement is used to make sure each if condition only runs once. Except for record which has to run continuously 
        record = 1
        
        #camara loop
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
                
                if k == 27: # press ESC if the scrips needs to be terminated prematurely 
                    terminate = 1
                    break
                
                if record == True: #recording is on and timestamps are recorded
                    frame_time = np.append(frame_time, frequency)
                    record_starting_time = time.time()
                    out.write(img)
                    frame_time = np.append(frame_time, time.time())
                    if first: #condition to let the user know that the recording has started and opens gate.
                        print('Starting recording..')
                        first = 0
                        opengate = 1
                
                if 5 < current_time - static_time < 6 and opengate: # switches short cut valve to off and GTCH to on
                    switchvalve()
                    print("GCTH open")
                    opengate = 0
                    print(current_time - static_time)
                
                if 8 < current_time - static_time < 9 and not opengate: #start flow in Cetoni elements
                    arduinoSer.write(b'1')
                    print("Flow has started")
                    opengate = 1
                    print(current_time - static_time)
                    
                if 10 < current_time - static_time < 11 and opengate: #start flow in Cetoni elements
                    arduinoSer.write(b'0')
                    print("Flow command terminated")
                    opengate = 0
                    print(current_time - static_time)
                    
                if 30 < current_time - static_time < 31 and not opengate: # switches short cut valve to on and GTCH to off
                    switchvalve()
                    print("GCTH closed")
                    opengate = 1
                    print(current_time - static_time)
                
                if 40 < current_time - static_time < 41 and opengate: # starts focusing
                    funcGen(freq = frequency, Amplitude = voltage)
                    print("focusing...")
                    imp_times = np.append(imp_times, time.time())
                    opengate = 0
                    print(current_time - static_time)
                    
                if current_time - static_time > 60 and not opengate: #stops focusing and initiales run stop
                    record = 0
                    opengate = 1
                    funcStop()
                    imp_times = np.append(imp_times, time.time())
                    print(current_time - static_time)
                        
                if not record and current_time - static_time > 55: #stops the recording and ends the run
                 
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
        if terminate:
            cv2.destroyAllWindows()
            break
## Closing everything
disconnect()
arduinoSer.write(b'0')
arduinoSer.close()
funcStop()