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

hzPlay = 100e6
# for infinite playback fill the entire 256MiByte memory, or 128Mi 16bits samples
nPlay = 128*1024*1024
rgwPlay = (c_uint16*int(nPlay))()

for i in range(len(rgwPlay)):
    rgwPlay[i] = i

print("Samples:"+str(nPlay)+" Rate:"+str(hzPlay)+"Hz "+" Period:"+str(nPlay/hzPlay)+"s")
dwf.FDwfDigitalOutPlayRateSet(hdwf, c_double(hzPlay)) # play sample rate

# enable play mode for the wanted signals
for i in range(0, 16):
    dwf.FDwfDigitalOutEnableSet(hdwf, c_int(i), c_int(1)) # enable
    dwf.FDwfDigitalOutTypeSet(hdwf, c_int(i), c_int(5)) # DwfDigitalOutTypePlay
    dwf.FDwfDigitalOutIdleSet(hdwf, c_int(i), DwfDigitalOutIdleLow)

# set play data array of 16 bit samples
dwf.FDwfDigitalOutPlayDataSet(hdwf, byref(rgwPlay), c_int(16), c_int(int(nPlay)))

print("Starting Digital Out...")
dwf.FDwfDigitalOutConfigure(hdwf, c_int(1))

dwf.FDwfDeviceCloseAll()
