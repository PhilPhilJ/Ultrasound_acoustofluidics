"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2021-08-24

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import time
import sys
import numpy
import matplotlib.pyplot as plt

if sys.platform.startswith("win"):
    dwf = cdll.LoadLibrary("dwf.dll")
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

hdwf = c_int()
szerr = create_string_buffer(512)
print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    print("failed to open device")
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0)) 

sts = c_byte()
reference = 1e3
freq = 1e3
start = -4.0
stop = 4.0
steps = 101

fOverride = True

print("Reference: "+str(reference)+" Ohm  Frequency: "+str(freq)+" Hz Offset: "+str(start)+" V ... "+str(stop)+" V")

dwf.FDwfAnalogImpedanceReset(hdwf)
dwf.FDwfAnalogImpedanceModeSet(hdwf, c_int(8)) # 0 = W1-C1-DUT-C2-R-GND, 1 = W1-C1-R-C2-DUT-GND, 8 = AD IA adapter
dwf.FDwfAnalogImpedanceReferenceSet(hdwf, c_double(reference)) # reference resistor value in Ohms
dwf.FDwfAnalogImpedanceFrequencySet(hdwf, c_double(freq)) # frequency in Hertz
dwf.FDwfAnalogImpedanceAmplitudeSet(hdwf, c_double(0.5)) # 0.5V amplitude = 1V peak2peak signal
dwf.FDwfAnalogImpedanceOffsetSet(hdwf, c_double(start)) # sets analog out and in channels to this offset
dwf.FDwfAnalogImpedanceConfigure(hdwf, c_int(0)) # configure 

if fOverride:
    dwf.FDwfAnalogInChannelOffsetSet(hdwf, c_int(0), c_double(start)) # set C1 offset to start
    dwf.FDwfAnalogInChannelOffsetSet(hdwf, c_int(1), c_double(0.0)) # set C2 offset
    dwf.FDwfAnalogInConfigure(hdwf, c_int(0)) # re-configure

time.sleep(1) # wait for the device, specially for the offsets to stabilize

rgOff = [0.0]*steps
rgRs = [0.0]*steps
rgXs = [0.0]*steps

for i in range(steps):
    vOff = start + i*(stop-start)/(steps-1)
    print("Step: "+str(i)+" "+str(vOff)+"V")
    rgOff[i] = vOff
    
    if fOverride:
        dwf.FDwfAnalogOutOffsetSet(hdwf, c_int(0), c_double(vOff)) # adjust analog out offset
        dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1)) # configure and start analog out
        dwf.FDwfAnalogInChannelOffsetSet(hdwf, c_int(0), c_double(vOff)) # set C1 offset to start
        dwf.FDwfAnalogInChannelOffsetSet(hdwf, c_int(1), c_double(0.0)) # set C2 offset
        dwf.FDwfAnalogInConfigure(hdwf, c_int(1)) # re-configure and start
    else:
        dwf.FDwfAnalogImpedanceOffsetSet(hdwf, c_double(vOff)) # adjust offset
        dwf.FDwfAnalogImpedanceConfigure(hdwf, c_int(1))
    
    time.sleep(0.01) # settle time depends on the offset step and DUT
    
    dwf.FDwfAnalogImpedanceStatus(hdwf, None) # ignore last capture 
    while True:
        if dwf.FDwfAnalogImpedanceStatus(hdwf, byref(sts)) == 0:
            dwf.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            quit()
        if sts.value == 2:
            break
            
    resistance = c_double()
    reactance = c_double()
    dwf.FDwfAnalogImpedanceStatusMeasure(hdwf, DwfAnalogImpedanceResistance, byref(resistance))
    dwf.FDwfAnalogImpedanceStatusMeasure(hdwf, DwfAnalogImpedanceReactance, byref(reactance))
    rgRs[i] = abs(resistance.value) # absolute value for logarithmic plot
    rgXs[i] = abs(reactance.value)
    
    for iCh in range(2):
        warn = c_int()
        dwf.FDwfAnalogImpedanceStatusWarning(hdwf, c_int(iCh), byref(warn))
        if warn.value:
            dOff = c_double()
            dRng = c_double()
            dwf.FDwfAnalogInChannelOffsetGet(hdwf, c_int(iCh), byref(dOff))
            dwf.FDwfAnalogInChannelRangeGet(hdwf, c_int(iCh), byref(dRng))
            if warn.value & 1:
                print("Out of range on Channel "+str(iCh+1)+" <= "+str(dOff.value - dRng.value/2)+"V")
            if warn.value & 2:
                print("Out of range on Channel "+str(iCh+1)+" >= "+str(dOff.value + dRng.value/2)+"V")

dwf.FDwfAnalogImpedanceConfigure(hdwf, c_int(0)) # stop
dwf.FDwfDeviceClose(hdwf)

plt.plot(rgOff, rgRs, rgOff, rgXs)
ax = plt.gca()
ax.set_yscale('log')
plt.show()

