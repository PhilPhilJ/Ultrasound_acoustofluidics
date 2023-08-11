"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2018-07-28

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import time
import sys
import numpy

# load dwf library
if sys.platform.startswith("win"):
    dwf = cdll.LoadLibrary("dwf.dll")
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

# print version information
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

hdwf = c_int()
szerr = create_string_buffer(512)
# try to connect to the first available device
print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

# print error message if connection fails
if hdwf.value == hdwfNone.value:
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    print("failed to open device")
    quit()

# configure impedance measurement
frequnecy = 1e3
reference = 1e3
print("Reference: "+str(reference)+" Ohm  Frequency: "+str(frequnecy/1e3)+" kHz for nanofarad capacitors")
dwf.FDwfAnalogImpedanceReset(hdwf)
dwf.FDwfAnalogImpedanceModeSet(hdwf, c_int(8)) # 0 = W1-C1-DUT-C2-R-GND, 1 = W1-C1-R-C2-DUT-GND, 8 = AD IA adapter
dwf.FDwfAnalogImpedanceReferenceSet(hdwf, c_double(reference)) # reference resistor value in Ohms
dwf.FDwfAnalogImpedanceFrequencySet(hdwf, c_double(frequnecy)) # frequency in Hertz
dwf.FDwfAnalogImpedanceAmplitudeSet(hdwf, c_double(1))
dwf.FDwfAnalogImpedanceConfigure(hdwf, c_int(1)) # start
time.sleep(1)

dwf.FDwfAnalogImpedanceStatus(hdwf, None) # ignore last capture, force a new one

sts = c_byte()
capacitance = c_double()
resistance = c_double()
reactance = c_double()

# measurement reading loop
for i in range(10):
    while True:
        if dwf.FDwfAnalogImpedanceStatus(hdwf, byref(sts)) == 0: # handle error
            dwf.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            quit()
        if sts.value == 2:
            break
    dwf.FDwfAnalogImpedanceStatusMeasure(hdwf, DwfAnalogImpedanceResistance, byref(resistance))
    dwf.FDwfAnalogImpedanceStatusMeasure(hdwf, DwfAnalogImpedanceReactance, byref(reactance))
    dwf.FDwfAnalogImpedanceStatusMeasure(hdwf, DwfAnalogImpedanceSeriesCapacitance, byref(capacitance))
    print(str(i)+" Resistance: "+str(resistance.value)+" Ohm  Reactance: "+str(reactance.value/1e3)+" kOhm  Capacitance: "+str(capacitance.value*1e9)+" nF")
    time.sleep(0.2)

dwf.FDwfAnalogImpedanceConfigure(hdwf, c_int(0)) # stop
dwf.FDwfDeviceClose(hdwf)
