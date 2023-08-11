"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-01-11

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import math
import time
import matplotlib.pyplot as plt
import sys
import numpy
from dwfconstants import *

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hzAcq = 1000
nSamples = 5000
rgSamples = (c_uint16*nSamples)()
print(rgSamples)


version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

print("Opening first device")
hdwf = c_int()
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    print("failed to open device")
    quit()

    
# generate counter
for i in range(0, 16):
    dwf.FDwfDigitalOutEnableSet(hdwf, c_int(i), c_int(1))
    dwf.FDwfDigitalOutDividerSet(hdwf, c_int(i), c_int(int((1<<i)*1000)))
    dwf.FDwfDigitalOutCounterSet(hdwf, c_int(i), c_int(10000), c_int(10000))

dwf.FDwfDigitalOutConfigure(hdwf, c_int(1))


dwf.FDwfDigitalInAcquisitionModeSet(hdwf, acqmodeScanScreen)
# sample rate = system frequency / divider
hzDI = c_double()
dwf.FDwfDigitalInInternalClockInfo(hdwf, byref(hzDI))
dwf.FDwfDigitalInDividerSet(hdwf, c_int(int(hzDI.value/hzAcq))) # 1kHz
# 16bit per sample format
dwf.FDwfDigitalInSampleFormatSet(hdwf, c_int(16))
# set number of sample to acquire
rgwSamples = (c_uint16*nSamples)()
dwf.FDwfDigitalInBufferSizeSet(hdwf, c_int(nSamples))

# begin acquisition
dwf.FDwfDigitalInConfigure(hdwf, c_int(0), c_int(1))


plt.axis([0, nSamples/hzAcq, 0, 16])
plt.yticks(numpy.arange(0, 16))
plt.ion()

rgx = numpy.arange(0, nSamples/hzAcq, 1.0/hzAcq)
plots = []
for c in range(16):
    plot, = plt.plot([], [])
    plot.set_xdata(rgx)
    plots.append(plot)

start = time.time()
print("Press Ctrl+C to stop")
try:
    while True: 
        sts = c_byte()
        dwf.FDwfDigitalInStatus(hdwf, c_int(1), byref(sts))
        cValid = c_int(0)
        dwf.FDwfDigitalInStatusSamplesValid(hdwf, byref(cValid))
        dwf.FDwfDigitalInStatusData(hdwf, byref(rgSamples), cValid.value*2) # 16bit samples = *2 bytes
        
        for c in range(16):
            rgb = (c_float*nSamples)()
            for i in range(cValid.value):
                rgb[i] = c + 0.8*((rgSamples[i]>>c)&1)
            plots[c].set_ydata(rgb)
        plt.draw()
        plt.pause(0.01)
except KeyboardInterrupt:
    pass

dwf.FDwfDeviceCloseAll()

