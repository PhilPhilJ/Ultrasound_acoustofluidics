"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2023-01-09

   Requires:                       
       Python 2.7, 3
   Generate pulses on trigger
"""

from ctypes import *
from dwfconstants import *
import math
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()
sts = c_byte()

dwf.FDwfParamSet(DwfParamOnClose, c_int(0)) # 0 = run, 1 = stop, 2 = shutdown

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))# 0 = the device will be configured only when calling FDwf###Configure


iChannel = 0
hzFreq = 1e6 # freq Hz
prcDuty = 25.0 # duty %
fPol = 1 # low or high, 0 or 1
cPulses = 8 
sWait = 1e-6

hzSys = c_double()
maxCnt = c_uint()
dwf.FDwfDigitalOutInternalClockInfo(hdwf, byref(hzSys))
dwf.FDwfDigitalOutCounterInfo(hdwf, c_int(0), 0, byref(maxCnt))

# for low frequencies use divider as pre-scaler to satisfy counter limitation of 32k
cDiv = int(math.ceil(hzSys.value/hzFreq/maxCnt.value))
# count steps to generate the give frequency
cPulse = int(round(hzSys.value/hzFreq/cDiv))
# duty
cHigh = int(cPulse*prcDuty/100)
cLow = int(cPulse-cHigh)

print("Generate: "+str(hzSys.value/cPulse/cDiv)+"Hz duty: "+str(100.0*cHigh/cPulse)+"% divider: "+str(cDiv))

dwf.FDwfDigitalOutEnableSet(hdwf, c_int(iChannel), c_int(1))
dwf.FDwfDigitalOutTypeSet(hdwf, c_int(iChannel), DwfDigitalOutTypePulse) # 
dwf.FDwfDigitalOutDividerSet(hdwf, c_int(iChannel), c_int(cDiv)) # max 2147483649, for counter limitation or custom sample rate
dwf.FDwfDigitalOutCounterSet(hdwf, c_int(iChannel), c_int(cLow), c_int(cHigh)) # max 32768
dwf.FDwfDigitalOutCounterInitSet(hdwf, c_int(iChannel), c_int(fPol), c_int(0)) 
dwf.FDwfDigitalOutRunSet(hdwf, c_double(1.0*cPulses*(cLow+cHigh)*cDiv/hzSys.value)) # seconds to run
dwf.FDwfDigitalOutWaitSet(hdwf, c_double(sWait)) # wait after trigger
dwf.FDwfDigitalOutRepeatSet(hdwf, c_int(0)) # infinite
dwf.FDwfDigitalOutRepeatTriggerSet(hdwf, c_int(1))

# trigger on Trigger IO 
dwf.FDwfDigitalOutTriggerSourceSet(hdwf, trigsrcExternal1)

# trigger on DIOs
#dwf.FDwfDigitalOutTriggerSourceSet(hdwf, trigsrcDetectorDigitalIn)
#dwf.FDwfDigitalInTriggerSet(hdwf, c_int(0), c_int(0), c_int(1<<1), c_int(0)) # DIO/DIN-1 rise
#dwf.FDwfDigitalInConfigure(hdwf, c_int(1), c_int(1))


print("Armed")
dwf.FDwfDigitalOutConfigure(hdwf, c_int(1))

dwf.FDwfDeviceCloseAll()
