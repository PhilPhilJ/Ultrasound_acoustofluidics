# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:50:42 2023

@author: s102772
"""
import sys
sys.path.append('C:/Users/s102772/Desktop/Ultrasound_acoustofluidics')
import cv2
from pypylon import pylon
import serial, time
import os
import numpy as np
from AD_func import Connect, disconnect, funcStop, funcGen
import pandas as pd
from Valve_control import switchvalve, CheckOpen


print('Press ESC to close the window')

arduinoSer = serial.Serial('COM3',baudrate=9600,timeout=0.5)
arduinoSer.write(b'0') # makes sure the flow is off

terminate = 0 #condition for breaking the for loop

#Connect to analog discovery
Connect()

#This part is used for sweep of a broad span of frequencies to change the estimated focus time according to the frequency
different_times = 0
if different_times:
    #time_a = np.linspace(30, 5, 50)
    #time_b = np.linspace(5, 30, 50)
    time_a = np.linspace(45, 25, 6)
    time_b = np.linspace(25, 5, 94)
    
    times = np.concatenate((time_a, time_b), axis=0)

#Use the split if frequencies in different regions are wanted
split_freq = 0
if split_freq:
    lower = np.linspace(1.8975 - 0.0055, 1.8975, 50)
    upper = np.linspace(1.8975, 1.8975 + 0.0055, 50)
    
    frequencies = np.concatenate((lower, upper), axis=0)
else:
    frequencies = np.linspace(2, 2.1 ,20)


for j in range(0,1):
    
    frequency = frequencies[j]    
    
    #if only single frequency is wanted
    single_frequecy = 0
    if single_frequecy == True:
        frequency = 1.898
        
    runs = 1
    
    for i in range(runs):
        
        # conecting to the first available camera
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        # Grabing Continusely (video) with minimal delay
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        
        newpath = r"C:/Users/s102772/Desktop/Mervan"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        #cap = cv2.VideoCapture(0) #VideoCapture object which stores the frames, the argument is just the device index (may be 0, or -1)
        size = (1440, 1080) # Camera resoloution: 4504x4504px, FPS: 18
        FPS = 20 # Frames per second of camera
        fourcc = cv2.VideoWriter_fourcc(*"mp4v") #Defines output format, mp4
        out = cv2.VideoWriter(newpath +
                            "run "  + str(j) + "." + str(i) +
                              '.mp4', fourcc, FPS, size, False) #Change path to saved location
        
        ##other parameters
        temp = "24 C"
        humid = "19%"
        gain = "10 dB"
        lamp = "10 V and 3.5 A"
        Alg_gen = 'Mix (1.1 + 3.2 + 3.21 + 2.3)'
        voltage = 5
        file = open(newpath + "run "  + str(j) + "." + str(i) +'.txt', 'w')
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
        frame_time = np.append(frame_time, voltage)
        #frame_time = np.append(frame_time, frequency) # Appends the frequecyto as the first value in the timestamps
        
        if different_times:
            estimated_focustime = times[i] #This is the time + 2 seconds that is the estimated time. Estimate this for each frequency
        else:
            estimated_focustime = 30
        
        #conditions used to control the if conditions
        first = True
        static_time = time.time()
        opengate = 1 # the "opengate" statement is used to make sure each if condition only runs once. Except for record which has to run continuously 
        record = 0
        
        if CheckOpen() == True:
            switchvalve()
            print("The GTCH was open and is now closed")
        
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
                
                if 2 < current_time - static_time < 3 and opengate: # switches short cut valve to off and GTCH to on
                    switchvalve()
                    print("GCTH open")
                    opengate = 0
                    print(current_time - static_time)
                
                if 3 < current_time - static_time < 4 and not opengate: #start flow in Cetoni elements
                    arduinoSer.write(b'1')
                    print("Flow has started")
                    opengate = 1
                    print(current_time - static_time)
                    
                if 5 < current_time - static_time < 6 and opengate: #start flow in Cetoni elements
                    arduinoSer.write(b'0')
                    print("Flow command terminated")
                    opengate = 0
                    print(current_time - static_time)
                    
                if 14 < current_time - static_time < 15 and not opengate: # switches short cut valve to on and GTCH to off
                    switchvalve()
                    print("GCTH closed")
                    opengate = 1
                    record = True
                    print(current_time - static_time)
                    
                if record == True: #recording is on and timestamps are recorded
                    record_starting_time = time.time()
                    out.write(img)
                    frame_time = np.append(frame_time, time.time())
                    if first: #condition to let the user know that the recording has started.
                        print('Starting recording..')
                        first = 0
                
                if 21 < current_time - static_time < 22 and opengate: # starts focusing
                    funcGen(freq = frequency, Amplitude = voltage)
                    print("focusing...")
                    imp_times = np.append(imp_times, time.time())
                    opengate = 0
                    print(current_time - static_time)
                    
                if current_time - static_time > 20 + estimated_focustime and not opengate: #stops focusing and initiales run stop
                    record = 0
                    funcStop()
                    print("focusing stoped")
                    opengate = 1
                    imp_times = np.append(imp_times, time.time())
                    print(current_time - static_time)
                        
                if not record and current_time - static_time > 22 + estimated_focustime + 2: #stops the recording and ends the run
                 
                        cv2.destroyAllWindows()
                        the_time = time.time()
                        df = pd.DataFrame({'Frame time':frame_time})
                        df2 = pd.DataFrame({'Important times':imp_times})
                        df.to_csv(newpath + "run"  + str(j) + "." + str(i) + " " + 'Frame time' + '.csv', sep=';', encoding='utf-8')
                        df2.to_csv(newpath + "run"  + str(j) + "." + str(i) + " " +'Important times' + '.csv', sep=';', encoding='utf-8')
                        file.close()
                        break
                
            grabResult.Release()
        
        # Releasing the resource    
        camera.StopGrabbing()
        out.release() 
    
        if terminate:
            cv2.destroyAllWindows()
            funcStop()
            if CheckOpen() == True:
                switchvalve()
                print("The GTCH was open and is now closed")
            break
    if terminate:
        break
## Closing everything
disconnect()
arduinoSer.write(b'0')
arduinoSer.close()
funcStop()