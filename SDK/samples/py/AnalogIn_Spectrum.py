"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-03-03

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import time
import matplotlib.pyplot as plt
import sys
import numpy

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

# prevent temperature drift
dwf.FDwfParamSet(DwfParamOnClose, c_int(0)) # 0 = run, 1 = stop, 2 = shutdown

hdwf = c_int()
print("Opening first device")
if dwf.FDwfDeviceOpen(-1, byref(hdwf)) != 1 or hdwf.value == hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(szerr.value)
    print("failed to open device")
    quit()

# 0 = the device will be configured only when calling FDwf?Configure
dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))


# capture up to 32Ki if samples
nBufMax = c_int()
dwf.FDwfAnalogInBufferSizeInfo(hdwf, 0, byref(nBufMax))
nSamples = min(32768, nBufMax.value)
print("Samples: "+str(nSamples)) 

#set up acquisition
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(100000000.0))
dwf.FDwfAnalogInBufferSizeSet(hdwf, nSamples)
dwf.FDwfAnalogInChannelEnableSet(hdwf, 0, 1)
dwf.FDwfAnalogInChannelEnableSet(hdwf, 1, 1)
dwf.FDwfAnalogInChannelRangeSet(hdwf, -1, c_double(2)) # 2V pk2pk

# wait at least 2 seconds for the offset to stabilize after the first connection
dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(0))
time.sleep(0.1)

print("Starting oscilloscope")
if dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1)) != 1 :
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(szerr.value)
    quit()

hzRate = c_double()
dwf.FDwfAnalogInFrequencyGet(hdwf, byref(hzRate))

while True:
    sts = c_byte()
    # fetch status and data from device
    if dwf.FDwfAnalogInStatus(hdwf, 1, byref(sts)) != 1 :
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(szerr.value)
        quit()
    if sts.value == DwfStateDone.value :
        break
print("Acquisition done")

rgdSamples1 = (c_double*nSamples)()
rgdSamples2 = (c_double*nSamples)()

dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples1, nSamples) # get channel 1 data
dwf.FDwfAnalogInStatusData(hdwf, 1, rgdSamples2, nSamples) # get channel 2 data
dwf.FDwfDeviceCloseAll()

plt.title("raw data")
plt.plot(numpy.fromiter(rgdSamples1, dtype = numpy.float), color='orange', label='C1')
plt.plot(numpy.fromiter(rgdSamples2, dtype = numpy.float), color='blue', label='C2')
plt.show()


hzTop = hzRate.value/2
rgdWindow = (c_double*nSamples)()
vBeta = c_double(1.0) # used only for Kaiser window
vNEBW = c_double() # noise equivalent bandwidth
dwf.FDwfSpectrumWindow(byref(rgdWindow), c_int(nSamples), DwfWindowFlatTop, vBeta, byref(vNEBW))

for i in range(nSamples):
    rgdSamples1[i] = rgdSamples1[i]*rgdWindow[i]
    rgdSamples2[i] = rgdSamples2[i]*rgdWindow[i]

plt.title("windowed data")
plt.plot(numpy.fromiter(rgdSamples1, dtype = numpy.float), color='orange', label='C1')
plt.plot(numpy.fromiter(rgdSamples2, dtype = numpy.float), color='blue', label='C2')
plt.show()


# Using power of two number of samples, BINs of samples/2+1, first 0.0 and last 1.0;
# otherwise it will be a more resource hungry algorithm used. 
# The first and last can limit the output frequency range.
# With 0/1 the BINs range from DC-0Hz to sample rate/2. With 0.2/0.5 the BINs will range from rate/10 to rate/4.
# The BIN output is peak voltage and phase in radian units.
iFirst = 0.0
iLast = 1.0
nBins = int(nSamples/2+1)
rgdBins1 = (c_double*nBins)()
rgdBins2 = (c_double*nBins)()
dwf.FDwfSpectrumTransform(byref(rgdSamples1), nSamples, byref(rgdBins1), None, nBins, c_double(iFirst), c_double(iLast))
dwf.FDwfSpectrumTransform(byref(rgdSamples2), nSamples, byref(rgdBins2), None, nBins, c_double(iFirst), c_double(iLast))

sqrt2 = math.sqrt(2)
for i in range(nBins): 
    rgdBins1[i] = 20.0*math.log10(rgdBins1[i]/sqrt2) # to dBV
    rgdBins2[i] = 20.0*math.log10(rgdBins2[i]/sqrt2) # to dBV

rgMHz = []
MHzFirst = hzTop*iFirst/1e6
MHzLast = hzTop*iLast/1e6
MHzStep = hzTop*(iLast-iFirst)/(nBins-1)/1e6
for i in range(nBins): 
    rgMHz.append(MHzFirst + MHzStep*i)

rgBins1 = numpy.fromiter(rgdBins1, dtype = numpy.float)
rgBins2 = numpy.fromiter(rgdBins2, dtype = numpy.float)

plt.title("FFT dBV / MHz")
plt.xlim([MHzFirst, MHzLast])
plt.ylim([-130.0, 20.0])
plt.plot(rgMHz, rgBins1, color='orange', label='C1')
plt.plot(rgMHz, rgBins2, color='blue', label='C2')
plt.show()
