"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2021-09-02

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import sys
import time

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

# check library loading errors
szerr = create_string_buffer(512)
dwf.FDwfGetLastErrorMsg(szerr)
if szerr[0] != b'\0':
    print(str(szerr.value))


hdwf = c_int()
cDevice = c_int()

# declare string variables
devicename = create_string_buffer(64)
serialnum = create_string_buffer(16)

# print(DWF version
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

# enumerate connected devices
dwf.FDwfEnum(c_int(0), byref(cDevice))
print("Number of Devices: "+str(cDevice.value))

# open devices
for iDevice in range(0, cDevice.value):
    dwf.FDwfEnumDeviceName(c_int(iDevice), devicename)
    dwf.FDwfEnumSN(c_int(iDevice), serialnum)
    print("------------------------------")
    print("Device "+str(iDevice+1)+" : ")
    print("\t" + str(devicename.value))
    print("\t" + str(serialnum.value))
    dwf.FDwfDeviceOpen(c_int(iDevice), byref(hdwf))
    if hdwf.value == 0:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(szerr.value)
        continue
    
    dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(14), c_int(0), c_double(0.5))
    #dwf.FDwfAnalogIOConfigure(hdwf)
    
    sz = ""
    t = c_double()
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 14, 1, byref(t)) # sec to dev
    sz += "To Device:   "+str(round(t.value*1e3,2))+"ms "
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 14, 3, byref(t)) # Bps to dev
    sz += str(round(t.value/1024/1024,2))+"MiBps "
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 14, 5, byref(t)) # Bytes to dev
    sz += str(t.value/1024/1024)+"MB\n"
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 14, 2, byref(t)) # sec from dev
    sz += "From Device: "+str(round(t.value*1e3,2))+"ms "
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 14, 4, byref(t)) # Bps from dev
    sz += str(round(t.value/1024/1024,2))+"MiBps "
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 14, 6, byref(t)) # Bytes from dev
    sz += str(t.value/1024/1024)+"MB\n"
    sz += "* 1 kiBps = 1024 Bps"
    print(sz)
    
    dwf.FDwfDeviceClose(hdwf)
    

# ensure all devices are closed
dwf.FDwfDeviceCloseAll()
