"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2023-03-23

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import math
import sys
import time

if sys.platform.startswith("win"):
    dwf = cdll.LoadLibrary("dwf.dll")
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

iAck  = c_int()
iCrc  = c_int()
uRead  = c_uint()


dwf.FDwfDigitalSwdRateSet(hdwf, c_double(1e6)) # 1MHz
dwf.FDwfDigitalSwdCkSet(hdwf, c_int(0)) # DIO-0
dwf.FDwfDigitalSwdIoSet(hdwf, c_int(1)) # DIO-1

print("SWD Reset")
dwf.FDwfDigitalSwdClear(hdwf, c_int(52), c_int(16)) 

for i in range(10):
    # Read                       1AP 0DP       A32         ACK           data   0ok 1error
    dwf.FDwfDigitalSwdRead(hdwf, c_int(0), c_int(0), byref(iAck), byref(uRead), byref(iCrc))
    if iAck.value == 1 or iAck.value != 2: # OK or not Wait
        print("SWD Read ACK:"+str(iAck.value)+" Data: "+hex(uRead.value)+" CRC: "+str(iCrc.value))
        break
    print("SWD Read ACK:"+str(iAck.value))

for i in range(10):
    # Write                       1AP 0DP       A32         ACK                 data
    dwf.FDwfDigitalSwdWrite(hdwf, c_int(1), c_int(0), byref(iAck), c_uint(0x12345678)) 
    print("SWD Write ACK:"+str(iAck.value))
    if iAck.value == 1 or iAck.value != 2: # OK or not Wait
        break
        

dwf.FDwfDeviceCloseAll()
