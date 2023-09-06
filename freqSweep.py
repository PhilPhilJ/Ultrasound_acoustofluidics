#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 14:53:09 2023

@author: joakimpihl
"""

import sys
sys.path.append('C:/Program Files (x86)/Digilent/WaveFormsSDK/samples/py')
#sys.path.append('/Applications/WaveForms.app/Contents/Resources/SDK/samples/py')
from ctypes import *
from dwfconstants import *
import numpy as np
import time


### Function for generating a frequency sweep

def freqSweep(shape=funcSine,start=1.89,stop=1.93,by=2,Amplitude=1,v_Offset=0):  
    # 0 = the device will be configured only when calling FDwf###Configure - One can for instance just change the freq and everything else will automatically be configured
    dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))
    
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_int(1))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, shape) # Sets the output function
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(Amplitude)) # Sets the signal amplitude in volts i.e. 1 = 1V
    dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(v_Offset)) # Sets the voltage offset
    
    frequencies = np.arange(start*10**6, stop*10**6+by*10**3, by*10**3)   # start and stop frequencies in MHz, the step frequency is in kHz
    
    for i in frequencies:
        dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(freq*10**6)) # Sets the frequency in Hz i.e. 1000 = 1kHz  
        dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1)) #This func configures/starts the device with the specified configuration.
        #######################################
        
        #Add in some clever image analysis here
        
        #######################################
        print('Analysis at' + str(i) + 'MHz is complete. The result is:' + 'Add the result is' + '. Going on to the next frequency...')
        time.sleep(5) #Generates frequency for 5s and then it goes on to the next frequency
        


    print("Generating frequency sweep starting at " + str(start) + "MHz" + " and stopping at" + str(stop) + "MHz." + "The frequency step size is: " + str(by))
   
    return 