#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:23:55 2023

@author: joakimpihl
"""

from ctypes import *
import time
from dwfconstants import *
import sys

#%


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
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(1.91*10**6)) # Sets the frequency in Hz i.e. 1000 = 1kHz
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1)) # Sets the signal amplitude in volts i.e. 1 = 1V
#dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1.41)) # Sets the voltage offset

print("Generating sine wave...")
dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1)) #This func configures/starts the device with the specified configuration.

#dwf.FDwfDeviceClose(hdwf)