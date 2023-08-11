#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:23:55 2023

@author: joakimpihl
"""

from ctypes import *
import time
import sys
#sys.path.append('C:/Program Files (x86)/Digilent/WaveFormsSDK/samples/py')
sys.path.append('/Applications/WaveForms.app/Contents/Resources/SDK/samples/py')
from dwfconstants import *
import cv2


# Checks if the system is windows (win) or Mac os (darwin) and then find path to dwf: /Library/Frameworks/dwf.framework/dwf
if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"): 
    dwf = cdll.LoadLibrary("/Applications/WaveForms.app/Contents/Frameworks/dwf.framework/dwf")

        
hdwf = c_int()
channel = c_int(0)


i = 1

while i>0:
    l = cv2.waitKey(0)
    img = cv2.imread('/Users/joakimpihl/Desktop/img1.jpeg')
    cv2.imshow('title', img)
    
    if l==102: # press f
        
        #Retrieves the API version
        #version = create_string_buffer(16)
        #dwf.FDwfGetVersion(version)
        #print("DWF Version: "+str(version.value))
        
        # Prevent temperature drift - Specifies Analog discovery behavior upon closure of the program
        dwf.FDwfParamSet(DwfParamOnClose, c_int(0)) # 0 = run, 1 = stop, 2 = shutdown
        
        #Open device
        print("Opening first device...")
        dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
        
        
        if hdwf.value == hdwfNone.value:
            print("failed to open device")
            quit()
        
        # 0 = the device will be configured only when calling FDwf###Configure - One can for instance just change the freq and everything else will automatically be configured
        dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))
        
        dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_int(1))
        dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcSine) # Sets the output function
        dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(1.91*10**6)) # Sets the frequency in Hz i.e. 1000 = 1kHz
        dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1)) # Sets the signal amplitude in volts i.e. 1 = 1V
        #dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1.41)) # Sets the voltage offset
        
        print("Generating sine wave...")
        dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1)) #This func configures/starts the device with the specified configuration.
        
        #dwf.FDwfDeviceClose(hdwf)
    elif l == 103: # press g
        print("Stopping sine wave...")
        dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(0)) # Stops the sine function
        #dwf.FDwfDeviceClose(hdwf)
    elif l == 27: # press esc
        break
        
        



#%%
'''
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)
'''

from pypylon import pylon
import serial, time
import cv2

import sys
sys.path.append('C:/Program Files (x86)/Digilent/WaveFormsSDK/samples/py')
from ctypes import *
from dwfconstants import *



print('Press ESC to close the window')

arduinoSer = serial.Serial('COM3',baudrate=9600,timeout=0.5)
flow_on = 0;

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

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
        if k == 27: # press ESC
            break
        if k == 32: # press spacebar  
            if flow_on==0:
                arduinoSer.write(b'1')
                flow_on = 1
            else:
                arduinoSer.write(b'0')
                flow_on = 0
        if k == 97: # press a (alive)
            arduinoSer.write(b'3') # on
        if k == 100: # press d (dead) 
            arduinoSer.write(b'2') # off

        # Checks if the system is windows (win) or Mac os (darwin) and then find path to dwf: /Library/Frameworks/dwf.framework/dwf
        if sys.platform.startswith("win"):
            dwf = cdll.dwf
        elif sys.platform.startswith("darwin"): 
            dwf = cdll.LoadLibrary("/Applications/WaveForms.app/Contents/Frameworks/dwf.framework/dwf")
            
        hdwf = c_int()
        channel = c_int(0)
        
        #% 
        #Retrieves the API version
        
        version = create_string_buffer(16)
        dwf.FDwfGetVersion(version)
        print("DWF Version: "+str(version.value))
        
        
        #%
        
        
        # Prevent temperature drift - Specifies Analog discovery behavior upon closure of the program
        dwf.FDwfParamSet(DwfParamOnClose, c_int(0)) # 0 = run, 1 = stop, 2 = shutdown
        
        #%
        
        #Open device
        print("Opening first device...")
        dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
        
        
        if hdwf.value == hdwfNone.value:
            print("failed to open device")
            quit()
        
        #%
        
        # 0 = the device will be configured only when calling FDwf###Configure - One can for instance just change the freq and everything else will automatically be configured
        dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))
        
        dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_int(1))
        dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcSine) # Sets the output function
        dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(1.1*10**6)) # Sets the frequency in Hz i.e. 1000 = 1kHz
        dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1)) # Sets the signal amplitude in volts i.e. 1 = 1V
        #dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1.41)) # Sets the voltage offset
        
        print("Generating sine wave...")
        dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1)) #This func configures/starts the device with the specified configuration.
        
        dwf.FDwfDeviceClose(hdwf)  
   
    grabResult.Release()
    
# Releasing the resource    
camera.StopGrabbing()

arduinoSer.write(b'0')

cv2.destroyAllWindows() 
arduinoSer.close()

#%%

