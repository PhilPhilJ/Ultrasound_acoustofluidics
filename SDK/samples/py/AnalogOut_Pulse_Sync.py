"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-05-31

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import time
from dwfconstants import *
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

# 0 = run, 1 = stop, 2 = shutdown
dwf.FDwfParamSet(DwfParamOnClose, c_int(0))

#open device
print("Opening first device...")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

# 0 = the device will be configured only when calling FDwf###Configure
dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0)) 

cntPulse = 2
hzPulse = 1e3

# enable two channels
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_int(True))
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_int(True))

# configure the enabled channels
dwf.FDwfAnalogOutIdleSet(hdwf, c_int(-1), DwfAnalogOutIdleInitial)
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(-1), AnalogOutNodeCarrier, funcPulse)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(-1), AnalogOutNodeCarrier, c_double(hzPulse))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(-1), AnalogOutNodeCarrier, c_double(3.3))

dwf.FDwfAnalogOutRunSet(hdwf, c_int(-1), c_double(cntPulse/hzPulse)) 
dwf.FDwfAnalogOutRepeatSet(hdwf, c_int(-1), c_int(1)) 

# set phase for the second channel
dwf.FDwfAnalogOutNodePhaseSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_double(90.0))

# configure and start
dwf.FDwfAnalogOutConfigure(hdwf, c_int(-1), c_int(1))

dwf.FDwfDeviceClose(hdwf)
