"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2020-12219

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

#open device
print("Opening first device...")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

# 0 = the device will be configured only when calling FDwf###Configure
dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))

# enable two channels
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_int(True))
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_int(True))
# for second channel set master the first channel
dwf.FDwfAnalogOutMasterSet(hdwf, c_int(1), c_int(0));
# slave channel is controlled by the master channel
# configure enabled channels
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(-1), AnalogOutNodeCarrier, funcSine) # CH1&2

rgFreq  = [60.0, 60.0, 60.0, 90.0]
rgAmp   = [ 1.0,  1.0,  1.5,  1.5]
rgPhase = [ 0.0, 30.0, 60.0, 90.0]

for i in range(len(rgFreq)):
    print("Step "+str(i+1)+" "+str(rgFreq[i])+"Hz "+str(rgAmp[i])+"V "+str(rgPhase[i])+"* ")
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(-1), AnalogOutNodeCarrier, c_double(rgFreq[i])) # CH1&2
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(-1), AnalogOutNodeCarrier, c_double(rgAmp[i])) # CH1&2
    dwf.FDwfAnalogOutNodePhaseSet(hdwf, c_int(1), AnalogOutNodeCarrier, c_double(rgPhase[i])) # CH2
    if i==0: 
        dwf.FDwfAnalogOutConfigure(hdwf, c_int(1), c_int(0)) # CH2 configure
        dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1)) # CH1 start
    else: 
        dwf.FDwfAnalogOutConfigure(hdwf, c_int(1), c_int(3)) # CH2 apply
        dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(3)) # CH1 apply
    time.sleep(5)

print("done")

dwf.FDwfDeviceClose(hdwf)
