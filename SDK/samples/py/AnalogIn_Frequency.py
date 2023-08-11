"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-11-10

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import time
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


print("Generating sine wave...")
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_int(1))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcSine)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(1e6))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(0.9))
dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1))



# capture up to 32Ki if samples
nBufMax = c_int()
dwf.FDwfAnalogInBufferSizeInfo(hdwf, 0, byref(nBufMax))
nSamples = min(32768, nBufMax.value)
nSamples = int(2**round(math.log2(nSamples)))

#set up acquisition
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(100e6))
dwf.FDwfAnalogInBufferSizeSet(hdwf, nSamples)
dwf.FDwfAnalogInChannelEnableSet(hdwf, 0, 1) # enable channel 0 (C1)
dwf.FDwfAnalogInChannelRangeSet(hdwf, 0, c_double(2)) # 2V pk2pk

if dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1)) != 1 :
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(szerr.value)
    quit()

hzRate = c_double()
dwf.FDwfAnalogInFrequencyGet(hdwf, byref(hzRate))
print("Samples: "+str(nSamples)+"  Rate: "+str(hzRate.value/1e6)+"MHz") 


rgdSamples = (c_double*nSamples)()
rgdWindow = (c_double*nSamples)()
nBins = int(nSamples/2+1)
rgdBins = (c_double*nBins)()
hzTop = hzRate.value/2
dwf.FDwfSpectrumWindow(byref(rgdWindow), c_int(nSamples), DwfWindowFlatTop, c_double(1.0), None)
print("Range: DC to "+str(hzTop/1e6)+" MHz  Resolution: "+str(hzTop/(nBins-1)/1e3)+" kHz") 

print("Press Ctrl+C to stop")
try:
    while True:
        time.sleep(0.5)
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
        for ich in range(2):
            dwf.FDwfAnalogInStatusData(hdwf, c_int(ich), rgdSamples, nSamples) # get channel 1 data
            for i in range(nSamples):
                rgdSamples[i] = rgdSamples[i]*rgdWindow[i]
            dwf.FDwfSpectrumFFT(byref(rgdSamples), nSamples, byref(rgdBins), None, nBins)

            iPeak = 0
            vPeak = float('-inf')
            for i in range(5, nBins): # skip DC lobe
                if rgdBins[i] < vPeak: continue
                vPeak = rgdBins[i]
                iPeak = i

            print("C"+str(ich+1)+" peak: "+str(hzTop*iPeak/(nBins-1)/1e6)+" MHz  "+str(vPeak)+" V")
            
            if iPeak < nBins-5: # weighted average
                s = 0
                m = 0
                for i in range(-4,5):
                    t = rgdBins[iPeak+i]
                    s += (iPeak+i)*t
                    m += t
                iPeak = s/m

            print("C"+str(ich+1)+" weighted: "+str(hzTop*iPeak/(nBins-1)/1e6)+" MHz")

except KeyboardInterrupt:
    pass

dwf.FDwfDeviceCloseAll()



