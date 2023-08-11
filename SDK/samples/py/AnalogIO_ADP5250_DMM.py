"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2018-07-19

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import time
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
print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(3), c_int(0), c_double(1.0)) # enable DMM
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(3), c_int(1), DwfDmmDCVoltage)
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(3), c_int(2), c_double(10)) # 10V range


# 10 times, once per second
for i in range(10):
    # wait between readings
    time.sleep(1)
    # fetch analog IO status from device
    if dwf.FDwfAnalogIOStatus(hdwf) == 0 :
        break;
    # get system monitor readings
    meas = c_double()
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(3), c_int(3), byref(meas))
    print("DMM DCV: " + str(meas.value) + "V")
    
#close the device
dwf.FDwfDeviceClose(hdwf)
