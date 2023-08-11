"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-09-06

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import time
from dwfconstants import *
import sys
import matplotlib.pyplot as plt
import numpy

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("Version: "+str(version.value))

cdevices = c_int()
dwf.FDwfEnum(c_int(0), byref(cdevices))
print("Number of Devices: "+str(cdevices.value))

if cdevices.value == 0:
    print("no device detected")
    quit()

print("Opening first device")
hdwf = c_int()
dwf.FDwfDeviceOpen(c_int(0), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

dwf.FDwfParamSet(DwfParamOnClose, c_int(1)) # 0 = run, 1 = stop, 2 = shutdown

print("Configure all analog out channels")
dwf.FDwfAnalogOutEnableSet(hdwf, c_int(-1), c_int(1)) # enable all channels
dwf.FDwfAnalogOutFunctionSet(hdwf, c_int(-1), funcDC)
dwf.FDwfAnalogOutOffsetSet(hdwf, c_int(-1), c_double(0.8)) # 800mV
dwf.FDwfAnalogOutConfigure(hdwf, c_int(-1), c_int(1))

print("Configure analog in")
cai = c_int()
dwf.FDwfAnalogInChannelCount(hdwf, byref(cai))
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(-1), c_int(1)) # enable all channels
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(2)) # 2 V peak to peak
dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(0))

print("Press Ctrl+C to stop")
try:
    while True:
        time.sleep(1.0)
        dwf.FDwfAnalogInStatus(hdwf, c_int(0), None)
        txt = ""
        for i in range(cai.value):
            v = c_double()
            dwf.FDwfAnalogInStatusSample(hdwf, c_int(i), byref(v))
            txt += "C%d %f\t" % (i+1, v.value)
        print(txt)
    
except KeyboardInterrupt:
    pass

dwf.FDwfDeviceCloseAll()


