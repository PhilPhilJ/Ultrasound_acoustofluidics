"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2018-07-23

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

dwf.FDwfParamSet(c_int(4), c_int(2)) # DwfParamOnClose run, keep device running on close, kee the SPI lines driven after close

print("Opening first device")
#dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
# device configuration of index 3 (4th) for Analog Discovery has 16kS digital-in/out buffer
dwf.FDwfDeviceConfigOpen(c_int(-1), c_int(3), byref(hdwf)) 
if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

print("Configuring SPI...")
dwf.FDwfDigitalSpiFrequencySet(hdwf, c_double(1e4))
dwf.FDwfDigitalSpiClockSet(hdwf, c_int(1))
dwf.FDwfDigitalSpiDataSet(hdwf, c_int(0), c_int(2)) # 0 DQ0_MOSI_SISO = DIO-2
dwf.FDwfDigitalSpiDataSet(hdwf, c_int(1), c_int(3)) # 1 DQ1_MISO = DIO-3
dwf.FDwfDigitalSpiModeSet(hdwf, c_int(0)) # SPI mode 
dwf.FDwfDigitalSpiOrderSet(hdwf, c_int(1)) # 1 MSB first
dwf.FDwfDigitalSpiSelectSet(hdwf, c_int(0), c_int(1)) # CS DIO-0, idle high
# cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad
#                                cDQ dual  bits 0    data 0
dwf.FDwfDigitalSpiWriteOne(hdwf, c_int(2), c_int(0), c_int(0)) # start driving the channels, clock and data
time.sleep(1)

fsCmd = c_uint16(0xABCB)
rgbTX = (c_ubyte*16)(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
rgwRX = (c_uint16*8)()

# 12bit command, 0x12D command, 0 dummy bits, 2 dual mode, 8bit words, word array, number of words
dwf.FDwfDigitalSpiCmdWrite(hdwf, c_int(12), c_int(0x12D), c_int(0), c_int(2), c_int(8), rgbTX, c_int(len(rgbTX))) 

# 16bit command, command, 0 dummy bits, 2 dual mode, 12bit words, read buffer, number of words
dwf.FDwfDigitalSpiCmdRead16(hdwf, c_int(16), fsCmd, c_int(0), c_int(2), c_int(12), rgwRX, c_int(len(rgwRX)))

dwf.FDwfDeviceCloseAll()
