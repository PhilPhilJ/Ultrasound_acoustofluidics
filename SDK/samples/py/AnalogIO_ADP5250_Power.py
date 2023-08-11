"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-05-24

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

hdwf = c_int()
sts = c_byte()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()
    
dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0)) # 0 = the device will be configured only when calling FDwf###Configure

# set up analog IO channel nodes
# enable p6V supply with 5V and 0.5A
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(0), c_double(1)) 
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(1), c_double(5.0)) 
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(2), c_double(0.5)) 
# enable p25V supply with 10V and 0.2A
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(0), c_double(1)) 
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(1), c_double(10.0)) 
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(2), c_double(0.2))
# enable n25V supply with -10V and -0.2A
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(2), c_int(0), c_double(1)) 
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(2), c_int(1), c_double(-10.0)) 
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(2), c_int(2), c_double(-0.2))
# master enable
dwf.FDwfAnalogIOEnableSet(hdwf, c_int(1))
dwf.FDwfAnalogIOConfigure(hdwf)

for i in range(1, 11):
    time.sleep(1) #wait 1 second between readings
    #fetch analogIO status from device
    if dwf.FDwfAnalogIOStatus(hdwf) == 0:
        break

    #supply monitor
    v1 = c_double()
    v2 = c_double()
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(0), c_int(1), byref(v1))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(0), c_int(2), byref(v2))
    print("p6V: " + str(round(v1.value,3)) + "V\t" + str(round(v2.value,3)) + "A")
    
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(1), c_int(1), byref(v1))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(1), c_int(2), byref(v2))
    print("p25V: " + str(round(v1.value,3)) + "V\t" + str(round(v2.value,3)) + "A")
    
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(2), c_int(1), byref(v1))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(2), c_int(2), byref(v2))
    print("n25V: " + str(round(v1.value,3)) + "V\t" + str(round(v2.value,3)) + "A")
    
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(4), c_int(0), byref(v1))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(4), c_int(3), byref(v2))
    print("Temp: " + str(round(v1.value,3)) + "*C Fan:\t" + str(round(v2.value,3)) + "RPM")

dwf.FDwfAnalogIOReset(hdwf)
dwf.FDwfAnalogIOConfigure(hdwf)

dwf.FDwfDeviceClose(hdwf)
