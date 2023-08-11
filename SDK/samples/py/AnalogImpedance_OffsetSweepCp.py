"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2021-08-25

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
reference = 10
freq = 10e3
start = -2.0
stop = 2.0
steps = 101

print("Reference: "+str(reference)+" Ohm  Frequency: "+str(freq)+" Hz Offset: "+str(start)+" V ... "+str(stop)+" V")

dwf.FDwfAnalogImpedanceReset(hdwf)
dwf.FDwfAnalogImpedanceModeSet(hdwf, c_int(8)) # 0 = W1-C1-DUT-C2-R-GND, 1 = W1-C1-R-C2-DUT-GND, 8 = AD IA adapter
dwf.FDwfAnalogImpedanceReferenceSet(hdwf, c_double(reference)) # reference resistor value in Ohms
dwf.FDwfAnalogImpedanceFrequencySet(hdwf, c_double(freq)) # frequency in Hertz
dwf.FDwfAnalogImpedanceAmplitudeSet(hdwf, c_double(1.0)) # 1.0V amplitude = 2V peak2peak signal
dwf.FDwfAnalogImpedanceOffsetSet(hdwf, c_double(start)) 
#dwf.FDwfAnalogImpedancePeriodSet(hdwf, c_int(128)) 
dwf.FDwfAnalogImpedanceConfigure(hdwf, c_int(1)) # start 

time.sleep(1) # wait for the device, specially for the offsets to stabilize

rgOff = [0.0]*steps
rgCp = [0.0]*steps

for i in range(steps):
    vOff = start + i*(stop-start)/(steps-1)
    print("Step: "+str(i)+" "+str(vOff)+"V")
    rgOff[i] = vOff
    dwf.FDwfAnalogImpedanceOffsetSet(hdwf, c_double(vOff)) # adjust offset
    dwf.FDwfAnalogImpedanceConfigure(hdwf, c_int(1))
    time.sleep(0.01) # settle time depends on the offset step and DUT
    
    dwf.FDwfAnalogImpedanceStatus(hdwf, None) # ignore last capture since we changed the offset
    while True:
        if dwf.FDwfAnalogImpedanceStatus(hdwf, byref(sts)) == 0:
            dwf.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            quit()
        if sts.value == 2:
            break
            
    Cp = c_double()
    dwf.FDwfAnalogImpedanceStatusMeasure(hdwf, DwfAnalogImpedanceParallelCapacitance, byref(Cp))
    rgCp[i] = Cp.value
    
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

plt.plot(rgOff, rgCp)
plt.show()

