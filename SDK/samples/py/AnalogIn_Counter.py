"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-03-22

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import time
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

#open device
"Opening first device..."
hdwf = c_int()
if dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf)) != 1 or hdwf.value == hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(szerr.value)
    print("failed to open device")
    quit()

# any internal or external trigger source can be used
if True:
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(100000000.0))
    dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcDetectorAnalogIn)
    dwf.FDwfAnalogInTriggerTypeSet(hdwf, trigtypeEdge)
    dwf.FDwfAnalogInTriggerChannelSet(hdwf, c_int(0)) # first channel
    dwf.FDwfAnalogInTriggerLevelSet(hdwf, c_double(0.0)) # 0.0V
    dwf.FDwfAnalogInTriggerConditionSet(hdwf, DwfTriggerSlopeRise) 
else:
    dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcExternal1)

timeout = 1.0 # frequency measurement refresh interval, 0 just count
countMax = c_double()
timeMax = c_double()
dwf.FDwfAnalogInCounterInfo(hdwf, byref(countMax), byref(timeMax))
dwf.FDwfAnalogInCounterSet(hdwf, c_double(timeout))
print("Max-Count: "+str(countMax.value)+"  Max-Timeout: "+str(timeMax.value)+"s  Timeout: "+str(timeout)+"s")

dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))

print("Press Ctrl+C to stop")
try:
    count2 = 0
    tick2 = 0
    countSum = 0
    while True:
        if timeout == 0: time.sleep(1)
        else: time.sleep(timeout/2)
            
        if dwf.FDwfAnalogInStatus(hdwf, c_int(0), None) != 1:
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            print(szerr.value)
            quit()
            
        count = c_double()
        freq = c_double()
        tick = c_int()
        dwf.FDwfAnalogInCounterStatus(hdwf, byref(count), byref(freq), byref(tick))

        if timeout == 0.0: # just count
            if count.value < count2: # counter rollover
                countSum += countMax.value+1
            print("Count: "+str(countSum+count.value))
        else: # frequency measurement
            if tick.value != tick2: # new measurement 
                countSum += count2 # sum earlier counts
                print("Count: "+str(countSum+count.value)+" Freq: "+str(freq.value)+"Hz")
        count2 = count.value
        tick2 = tick.value
        
except KeyboardInterrupt:
    pass


dwf.FDwfDeviceCloseAll()
