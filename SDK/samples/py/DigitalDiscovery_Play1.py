"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2021-09-10

   Requires:           
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import sys
import numpy


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

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))# 0 = the device will be configured only when calling FDwf###Configure

print("Configuring Digital Out...")

hzPlay = 1e6
# for infinite playback fill the entire 2GiBit of memory
data_py=[1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
# how many bytes we need to fit this many bits, (+7)/8
rgbData=(c_ubyte*((len(data_py)+7)>>3))(0) 

nSamples = len(data_py)
# array to bits in byte array
for i in range(nSamples):
    if data_py[i] != 0:
        rgbData[i>>3] |= 1<<(i&7)


print("Samples:"+str(nSamples)+" Rate:"+str(hzPlay)+"Hz "+" Period:"+str(nSamples/hzPlay)+"s")
dwf.FDwfDigitalOutPlayRateSet(hdwf, c_double(hzPlay)) # play sample rate

# enable play mode for DIO-24
dwf.FDwfDigitalOutEnableSet(hdwf, c_int(0), c_int(1)) # enable
dwf.FDwfDigitalOutTypeSet(hdwf, c_int(0), c_int(5)) # DwfDigitalOutTypePlay
dwf.FDwfDigitalOutIdleSet(hdwf, c_int(0), DwfDigitalOutIdleLow)
dwf.FDwfDigitalOutRunSet(hdwf, c_double(nSamples/hzPlay)) # run length

# set play data array of 16 bit samples
dwf.FDwfDigitalOutPlayDataSet(hdwf, byref(rgbData), c_int(1), c_int(int(nSamples)))

print("Starting Digital Out...")
dwf.FDwfDigitalOutConfigure(hdwf, c_int(1))

dwf.FDwfDeviceCloseAll()
