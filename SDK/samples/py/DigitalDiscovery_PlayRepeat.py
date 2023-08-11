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
nSamples = 256
rgbSamples= (c_ubyte*int(nSamples))()

for i in range(len(rgbSamples)):
    rgbSamples[i] = i


# 1. wait-run-repeat
# it should be a minimum of 1us idle between restarts, use wait and/or trigger
# dwf.FDwfDigitalOutWaitSet(hdwf, c_double(1e-6)) 
# dwf.FDwfDigitalOutRepeatSet(hdwf, c_int(2))

# 2. trigger on DIO/DIN 
# dwf.FDwfDigitalInBufferSizeSet(hdwf, c_int(0))
# dwf.FDwfDigitalInInputOrderSet(hdwf, c_int(1)) # 1 is DIO first, analog-in sample and trigger order bits is [0..31] [DIO-24..39,DIN-0..15]
# dwf.FDwfDigitalInTriggerSet(hdwf, c_uint(0), c_uint(0), c_uint(1<<15), c_uint(0)) # rising edge of 15 which is DIO 39
# dwf.FDwfDigitalInConfigure(hdwf, c_int(1), c_int(0)) 
# dwf.FDwfDigitalOutTriggerSourceSet(hdwf, trigsrcDetectorDigitalIn)

# 3. software trigger
dwf.FDwfDigitalOutTriggerSourceSet(hdwf, trigsrcPC)


dwf.FDwfDigitalOutRunSet(hdwf, c_double(nSamples / float(hzPlay)))
dwf.FDwfDigitalOutRepeatSet(hdwf, c_int(0)) # infinite repeats
dwf.FDwfDigitalOutRepeatTriggerSet(hdwf, c_int(1)) # in each cycle wait for the trigger if specified


# enable play mode for the wanted signals
for i in range(8):
    dwf.FDwfDigitalOutEnableSet(hdwf, c_int(i), c_int(1)) # enable
    dwf.FDwfDigitalOutTypeSet(hdwf, c_int(i), DwfDigitalOutTypePlay)
    dwf.FDwfDigitalOutIdleSet(hdwf, c_int(i), DwfDigitalOutIdleLow)

print("Samples:"+str(nSamples)+" Rate:"+str(hzPlay)+"Hz "+" Period:"+str(nSamples/hzPlay)+"s")
dwf.FDwfDigitalOutPlayRateSet(hdwf, c_double(hzPlay)) # play sample rate
# set play data array of 8 bit samples
dwf.FDwfDigitalOutPlayDataSet(hdwf, byref(rgbSamples), c_int(8), c_int(int(nSamples)))


print("Arming Digital Out...")
dwf.FDwfDigitalOutConfigure(hdwf, c_int(1))

# generate software trigger 
for i in range(5):
    time.sleep(1)
    print("run "+str(i+1))
    dwf.FDwfDeviceTriggerPC(hdwf)


dwf.FDwfDeviceCloseAll()
