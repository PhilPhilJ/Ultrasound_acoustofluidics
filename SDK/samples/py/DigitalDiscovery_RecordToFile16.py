"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2020-03-02

   Requires:           
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import sys
import time
import matplotlib.pyplot as plt
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

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))# 0 = the device will be configured only when calling FDwf###Configure

print("Configuring Digital In...")

# divider sampling by
divSample = 80 # 10MHz = 800Mhz/80, max ~40MBps, ~20M UShort / s

#samples to capture
nRecord = int(1e9)

cAvailable = c_int()
cLost = c_int()
cCorrupted = c_int()
fLost = 0
fCorrupted = 0
hzDI = c_double()
iRecord = int(0)

dwf.FDwfDigitalInInternalClockInfo(hdwf, byref(hzDI))
print("Base freq: "+str(hzDI.value/1e6)+"Mhz")
print("Sampling freq: "+str(hzDI.value/divSample/1e6)+"MHz")
print("Samples: "+str(nRecord))

# in record mode samples after trigger are acquired only
dwf.FDwfDigitalInAcquisitionModeSet(hdwf, acqmodeRecord)
# sample rate = system frequency / divider
dwf.FDwfDigitalInDividerSet(hdwf, c_int(divSample))
# 8bit per sample format
dwf.FDwfDigitalInSampleFormatSet(hdwf, c_int(16))
# number of samples after trigger
dwf.FDwfDigitalInTriggerPositionSet(hdwf, c_int(0))
# trigger when all digital pins are low
dwf.FDwfDigitalInTriggerSourceSet(hdwf, trigsrcNone)
# for Digital Discovery 
# with order 0: DIN0:7;   with 32 bit sampling [DIN0:23  + DIO24:31]
# with order 1: DIO24:31; with 32 bit sampling [DIO24:39 + DIN0:15]
dwf.FDwfDigitalInInputOrderSet(hdwf, c_int(0))
# begin acquisition
dwf.FDwfDigitalInConfigure(hdwf, c_int(1), c_int(1))

print("Recording...")

file = open("record.bin", "wb")

while True:
    if dwf.FDwfDigitalInStatus(hdwf, c_int(1), byref(sts)) == 0:
        print("Error")
        break
    
    dwf.FDwfDigitalInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
    
    if cLost.value :
        fLost = 1
    if cCorrupted.value :
        fCorrupted = 1

    if cAvailable.value == 0:
        break
    
    cChunk = min(cAvailable.value, nRecord-iRecord)

    # print(str(iRecord)+" "+str(cChunk))
    
    rgBuffer = (c_uint16*cChunk)()
    
    dwf.FDwfDigitalInStatusData(hdwf, byref(rgBuffer), c_int(2*cChunk))
    
    file.write(numpy.fromiter(rgBuffer, dtype = numpy.ushort))

    iRecord += cChunk

    if iRecord >= nRecord:
        print("Done")
        break

dwf.FDwfDeviceClose(hdwf)

file.close()

if fLost != 0:
    print("Samples were lost! Reduce sample rate")
if fCorrupted != 0:
    print("Samples could be corrupted! Reduce sample rate")

