"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-11-09

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
voltage = c_double()
current = c_double()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

#open device
print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

# set up analog IO channel nodes

# enable fixed supply supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(0), c_double(True)) 
# set voltage between 1V and 5V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(1), c_double(4.5)) 
# set current limitation between 10mA and 3A
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(2), c_double(2.0)) 

# enable positive supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(0), c_double(True)) 
# set voltage between -1V and -15V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(1), c_double(-12.0)) 
# set current limitation between -10mA and -500mA
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(2), c_double(-0.4)) 

# enable negative supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(2), c_int(0), c_double(True)) 
# set voltage between 0 and 15V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(2), c_int(1), c_double(12.0)) 
# set current limitation between 10mA and 500mA
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(2), c_int(2), c_double(0.4))


# master enable
dwf.FDwfAnalogIOEnableSet(hdwf, c_int(True))

for i in range(1, 11):
    # wait between readings
    time.sleep(1)
    # fetch analogIO status from device
    if dwf.FDwfAnalogIOStatus(hdwf) == 0:
        break

    # fixed supply supply readings
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(0), c_int(1), byref(voltage))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(0), c_int(2), byref(current))
    print("O1: " + str(round(voltage.value,3)) + "V\t" + str(round(current.value,3)) + "A")

    # positive supply supply readings
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(1), c_int(1), byref(voltage))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(1), c_int(2), byref(current))
    print("O2: " + str(round(voltage.value,3)) + "V\t" + str(round(current.value,3)) + "A")

    # negative supply supply readings
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(2), c_int(1), byref(voltage))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(2), c_int(2), byref(current))
    print("O3: " + str(round(voltage.value,3)) + "V\t" + str(round(current.value,3)) + "A")


# close the device
dwf.FDwfDeviceClose(hdwf)
