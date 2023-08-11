"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2021-10-20

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
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
# device configuration of index 3 (4th) for Analog Discovery has 16kS digital-in/out buffer
#dwf.FDwfDeviceConfigOpen(c_int(-1), c_int(3), byref(hdwf)) 

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

print("Starting I2C Spy...")

dwf.FDwfDigitalI2cRateSet(hdwf, c_double(1e5)) # 100kHz
dwf.FDwfDigitalI2cSclSet(hdwf, c_int(0)) # SCL = DIO-0
dwf.FDwfDigitalI2cSdaSet(hdwf, c_int(1)) # SDA = DIO-1
dwf.FDwfDigitalI2cSpyStart(hdwf)

nData = 16
fStart = c_int()
fStop = c_int()
rgData = (c_ubyte*nData)()
cData = c_int()
iNak = c_int()

try:
    while True:
        cData.value = nData
        if dwf.FDwfDigitalI2cSpyStatus(hdwf, byref(fStart), byref(fStop), byref(rgData), byref(cData), byref(iNak)) == 0:
            print("Communication with the device failed.")
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            break
        
        msg = []
        if fStart.value == 1: 
            msg.append("Start")
        elif fStart.value == 2:
            msg.append("ReStart")
            
        for i in range(cData.value):
            # first data is address when fStart is not zero
            if i == 0 and fStart.value != 0:
                msg.append(hex(rgData[i]>>1))
                if rgData[i]&1:
                    msg.append("RD")
                else:
                    msg.append("WR")
            else:
                msg.append(hex(rgData[i]))
                
        if fStop.value != 0: 
            msg.append("Stop")
        
        # NAK of data index + 1 or negative error
        if iNak.value > 0: 
            msg.append("NAK: "+str(iNak.value))
        elif iNak.value < 0:
            msg.append("Error: "+str(iNak.value))
        
        if len(msg):
            print(msg)
            
        time.sleep(0.001)
        
except KeyboardInterrupt: # Ctrl+C
    pass



dwf.FDwfDeviceCloseAll()
