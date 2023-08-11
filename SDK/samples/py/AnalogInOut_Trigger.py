"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-10-04

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import time
import sys
import matplotlib.pyplot as plt
import numpy


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()
sts = c_byte()
rgdSamples = (c_double*8192)()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    szError = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szError);
    print("failed to open device\n"+str(szError.value))
    quit()

#                                    AWG 1     carrier
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(0), c_int(1))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), c_int(0), funcSine)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), c_int(0), c_double(234))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), c_int(0), c_double(2.0))
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(1), c_int(1)) # FM
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), c_int(1), funcSine)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), c_int(1), c_double(12))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), c_int(1), c_double(20.0)) # 20%
dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1))

#set up acquisition
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(1e6))
dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(8192)) 
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_int(1))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))

#set up trigger
dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcAnalogOut1) 

dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

plt.axis([0, len(rgdSamples), -2.5, 2.5])
plt.ion()
hl, = plt.plot([], [])
hl.set_xdata(range(0, len(rgdSamples)))

try:
    while True:
        # new acquisition is started automatically after done state 
        while True:
            dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
            if sts.value == DwfStateDone.value :
                break
            time.sleep(0.001)
        
        dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples, 8192) # get channel 1 data
        
        hl.set_ydata(rgdSamples)
        plt.draw()
        plt.pause(0.1)
except:
    pass
    
dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(0))
dwf.FDwfDeviceCloseAll()

