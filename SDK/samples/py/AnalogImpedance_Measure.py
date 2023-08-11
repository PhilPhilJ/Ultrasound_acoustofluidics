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


rgMeasure = [[DwfAnalogImpedanceImpedance,"Impedance","Ohm"],
    [DwfAnalogImpedanceImpedancePhase,"ImpedancePhase","Radian"],
    [DwfAnalogImpedanceResistance,"Resistance","Ohm"],
    [DwfAnalogImpedanceReactance,"Reactance","Ohm"],
    [DwfAnalogImpedanceAdmittance,"Admittance","S"],
    [DwfAnalogImpedanceAdmittancePhase,"AdmittancePhase","Radian"],
    [DwfAnalogImpedanceConductance,"Conductance","S"],
    [DwfAnalogImpedanceSusceptance,"Susceptance","S"],
    [DwfAnalogImpedanceSeriesCapacitance,"SeriesCapacitance","F"],
    [DwfAnalogImpedanceParallelCapacitance,"ParallelCapacitance","F"],
    [DwfAnalogImpedanceSeriesInductance,"SeriesInductance","H"],
    [DwfAnalogImpedanceParallelInductance,"ParallelInductance","H"],
    [DwfAnalogImpedanceDissipation,"Dissipation","X"],
    [DwfAnalogImpedanceQuality,"Quality","X"],
    [DwfAnalogImpedanceVrms,"Vrms","V"],
    [DwfAnalogImpedanceVreal,"Vreal","V"],
    [DwfAnalogImpedanceVimag,"Vimag","V"],
    [DwfAnalogImpedanceIrms,"Irms","A"],
    [DwfAnalogImpedanceIreal,"Ireal","A"],
    [DwfAnalogImpedanceIimag,"Iimag","A"]]


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


# measurement reading loop
while True:
    sts = c_byte()
    if dwf.FDwfAnalogImpedanceStatus(hdwf, byref(sts)) == 0: # handle error
        dwf.FDwfGetLastErrorMsg(szerr)
        print(str(szerr.value))
        quit()
    if sts.value == 2:
        break

for meas in rgMeasure:
    cval = c_double()
    dwf.FDwfAnalogImpedanceStatusMeasure(hdwf, meas[0], byref(cval))
    val = cval.value
    scale = ""
    if meas[2] != "Radian":
        if abs(val)>=1e9:
            val /= 1e9
            scale = "G"
        elif abs(val)>=1e6:
            val /= 1e6
            scale = "M"
        elif abs(val)>=1e3:
            val /= 1e3
            scale = "k"
        elif abs(val)<1e-9:
            val *= 1e12
            scale = "p"
        elif abs(val)<1e-6:
            val *= 1e9
            scale = "n"
        elif abs(val)<1e-3:
            val *= 1e6
            scale = "u"
        elif abs(val)<1:
            val *= 1e3
            scale = "m"
    print(meas[1]+": "+str(val)+" "+scale+meas[2])


dwf.FDwfAnalogImpedanceConfigure(hdwf, c_int(0)) # stop
dwf.FDwfDeviceClose(hdwf)
