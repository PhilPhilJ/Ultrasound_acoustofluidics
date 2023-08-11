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
dwf.FDwfDigitalSpiFrequencySet(hdwf, c_double(1e3))
dwf.FDwfDigitalSpiClockSet(hdwf, c_int(1))
dwf.FDwfDigitalSpiDataSet(hdwf, c_int(0), c_int(2)) # 0 DQ0_MOSI_SISO = DIO-2
dwf.FDwfDigitalSpiModeSet(hdwf, c_int(0)) # SPI mode 
dwf.FDwfDigitalSpiOrderSet(hdwf, c_int(1)) # 1 MSB first
dwf.FDwfDigitalSpiSelectSet(hdwf, c_int(0), c_int(1)) # CS DIO-0, idle high

# cDQ 0 SISO, 1 MOSI/MISO, 2 dual, 4 quad
#                                cDQ       bits 0    data 0
dwf.FDwfDigitalSpiWriteOne(hdwf, c_int(0), c_int(0), c_int(0)) # start driving the channels
time.sleep(1)

rgwRX1 = (c_uint16*10)()
rgwRX2 = (c_uint16*20)()
dw = c_uint32()

# 0 SISO mode, 16bit words, word
dwf.FDwfDigitalSpiWriteOne(hdwf, c_int(0), c_int(16), c_uint(0x1234))

# 16bit command, 0x1234 command, 0 dummy bits, 0 SISO mode, 24bit word, pointer to read variable
dwf.FDwfDigitalSpiCmdReadOne(hdwf, c_int(16), c_uint(0x1234), c_int(0), c_int(0), c_int(24), byref(dw))

dwf.FDwfDigitalSpiSelect(hdwf, c_int(0), c_int(0)) # Select software control DIO-0 = 0
dwf.FDwfDigitalSpiWriteOne(hdwf, c_int(0), c_int(16), c_uint(0x1234))) # write 16 bits
# 0 SISO mode, 12bit words, read buffer, number of words
dwf.FDwfDigitalSpiRead16(hdwf, c_int(0), c_int(12), rgwRX1, c_int(len(rgwRX1)))
dwf.FDwfDigitalSpiRead16(hdwf, c_int(0), c_int(12), rgwRX2, c_int(len(rgwRX2)))
dwf.FDwfDigitalSpiSelect(hdwf, c_int(0), c_int(1)) # Select software control DIO-0 = 1

dwf.FDwfDeviceCloseAll()
