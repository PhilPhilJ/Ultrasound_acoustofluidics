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
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define functions
# Function to find the mean value of the frame
def mean_value(frame, ratio=0.2):
    center_col = frame.shape[1] // 2
    left_col = int(center_col - (center_col * ratio))
    right_col = int(center_col + (center_col * ratio))
    cropped_frame = np.concatenate([frame[:, :left_col], frame[:, right_col:]])
        
    mean_value = np.mean(cropped_frame)

    return mean_value

# Function to check if the gradient of the last 10 values is less than 0.01
def end_fit(norm_intensities):
    if len(norm_intensities) > 10:
        gradient = np.diff(norm_intensities[-10:])
        mean_gradient = np.mean(gradient) 
        if abs(mean_gradient) < 5*10**(-6):
            return True
        else:
            return False

# Function to fit the data to the function
def func(t, t_star, R, ratio=0.2):
    k = np.pi*(1-ratio)/2
    return 1 - R/k * np.arctan(np.tan(k) * np.exp(-t/t_star))



print('Press ESC to close the window')

arduinoSer = serial.Serial('COM3',baudrate=9600,timeout=0.5)
arduinoSer.write(b'0') # makes sure the flow is off

terminate = 0 #condition for breaking the for loop

#Connect to analog discovery
Connect()

fitting_parameters = np.array([[],[]]) # array to store the fitting parameters

frequency = 1.8975 # frequency in MHz  
runs = 2
    
for i in range(runs):

    # Define array to store the mean values
    mean_values = np.array([])
        
    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        
    newpath = r'C:/Users/s102772/Desktop/Test'#r"D:/New Script/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
    #cap = cv2.VideoCapture(0) #VideoCapture object which stores the frames, the argument is just the device index (may be 0, or -1)
    size = (1440, 1080) # Camera resoloution: 4504x4504px, FPS: 18
    FPS = 20 # Frames per second of camera
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") #Defines output format, mp4
    out = cv2.VideoWriter(newpath +
                            "run " + str(i) +
                            '.mp4', fourcc, FPS, size, False) #Change path to saved location
        
    ##other parameters
    temp = "24 C"
    humid = "19%"
    gain = "10 dB"
    lamp = "10 V and 3.5 A"
    Alg_gen = 'Mix (1.1 + 3.2 + 3.21 + 2.3)'
    voltage = 1
    file = open(newpath + "run " + str(i) +'.txt', 'w')
    file.write("Temperature =" + str(temp) + 
                ", humidity =" + str(humid) + 
                ", Gain =" + str(gain) + 
                ", Light =" + str(lamp) + 
                ", Algae generation = " + str(Alg_gen) + 
                ". The voltage is: " +str(voltage) + 
                ". Frequency = " +str(frequency)) #Writes the info file change parameters before a run
    file.close()
        
    #Create timestaps and points of focus stat/stop
    frame_time = np.array([])
    frame_time = np.append(frame_time, frequency) # Appends the frequency as the first value in the timestamps
    mean_values = np.array([])
        
    estimated_focustime = 6
        
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
            cv2.namedWindow('Live view', cv2.WINDOW_NORMAL)
            cv2.imshow('Live view', img)
            k = cv2.waitKey(1)
                
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
                mean_values = np.append(mean_values, mean_value(img))
                if first: #condition to let the user know that the recording has started.
                    print('Starting recording..')
                    first = 0
                
            if 21 < current_time - static_time < 22 and opengate: # starts focusing
                if 'start_index' not in globals():
                    start_index = len(frame_time)
                funcGen(freq = frequency, Amplitude = voltage)
                print("focusing...")
                opengate = 0
                print(current_time - static_time)

            

            if 'start_index' in globals() and end_fit(mean_values) and not opengate: #stops focusing and initiales run stop
                record = 0
                funcStop()
                print("focusing stoped")
                opengate = 1
                print(current_time - static_time)
                        
            if not record and end_fit(mean_values): #stops the recording and ends the run
                mean_values = mean_values/mean_values[-1]
                t = frame_time[1:] - frame_time[start_index]
                popt, pcov = curve_fit(func, t[start_index:], mean_values[start_index:], p0=[1, 0.005], bounds=([0, 0], [10, 0.05]))
                fitting_parameters = np.append(fitting_parameters, popt)
                cv2.destroyAllWindows()
                the_time = time.time()
                df = pd.DataFrame({'Frame time':frame_time})
                
                plt.figure(figsize=(10, 7.5), dpi=300)  # Set the figure size and dpi
                plt.plot(t, mean_values, 'ro',label='Data')
                plt.plot(t, func(t, *popt), color='black', label='Fit')
                plt.axvline(x=0, color='black', linestyle='--', label='_nolabel_')
                plt.legend(loc='lower right')
                plt.savefig(f'C:/Users/s102772/Desktop/Test/Run {i}.png')  # Save the plot as 'plot.png'
                #df3 = pd.DataFrame({'Fitting parameters (t*)':popt[0], 'Fitting parameters (R)':popt[1]})
                #df.to_csv(newpath + "run"  + str(i) + " " + 'Frame time' + '.csv', sep=';', encoding='utf-8')
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
#if terminate:
#   break
## Closing everything
disconnect()
arduinoSer.write(b'0')
arduinoSer.close()
funcStop()