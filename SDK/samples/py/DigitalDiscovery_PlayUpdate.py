"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-02-11

   Requires:           
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import sys
import math
import time


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()
sts = c_ubyte()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

dwf.FDwfParamSet(DwfParamOnClose, c_int(1)) # 0 = run, 1 = stop, 2 = shutdown

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))# 0 = the device will be configured only when calling FDwf###Configure

print("Configuring Digital Out...")

hzPlay = 10e6
# for infinite playback fill the entire 256MiByte memory
nSamples = 13
rgbSamples = (c_ubyte*int(math.ceil(nSamples/2)))(0)

# 4bit counter stored in 8bit array
for i in range(nSamples):
    if i&1 == 0:
        rgbSamples[int(i/2)] = i
    else:
        rgbSamples[int(i/2)] |= i<<4

dwf.FDwfDigitalOutRunSet(hdwf, c_double(nSamples / float(hzPlay)))
dwf.FDwfDigitalOutRepeatSet(hdwf, c_int(1)) # once

# enable play mode for the wanted signals
for i in range(4):
    dwf.FDwfDigitalOutEnableSet(hdwf, c_int(i), c_int(1)) # enable
    dwf.FDwfDigitalOutTypeSet(hdwf, c_int(i), DwfDigitalOutTypePlay)
    dwf.FDwfDigitalOutIdleSet(hdwf, c_int(i), DwfDigitalOutIdleLow)

print("Samples:"+str(nSamples)+" Rate:"+str(hzPlay)+"Hz "+" Period:"+str(nSamples/hzPlay)+"s")
dwf.FDwfDigitalOutPlayRateSet(hdwf, c_double(hzPlay)) # play sample rate
# set play data array of 4 bit samples
dwf.FDwfDigitalOutPlayDataSet(hdwf, byref(rgbSamples), c_int(4), c_int(nSamples))

print("Starting Digital Out...")
# 0 1 2 3 4 5 ... 12
dwf.FDwfDigitalOutConfigure(hdwf, c_int(1))
time.sleep(1)

print("Changing some bits are starting again...")
# for performance when using a lot of samples align and use multiple of 64bits
dwf.FDwfDigitalOutPlayUpdateSet(hdwf, byref(rgbSamples), c_int(2), c_int(3)) # replace 2,3,4 with 0,1,2
# 0 1 0 1 2 5 ... 12
dwf.FDwfDigitalOutConfigure(hdwf, c_int(1))
time.sleep(1)

dwf.FDwfDeviceCloseAll()
