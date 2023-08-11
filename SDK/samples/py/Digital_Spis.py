"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2023-02-06

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import math
import sys
import time
import numpy
from dwfconstants import *


if sys.platform.startswith("win"):
    dwf = cdll.LoadLibrary("dwf.dll")
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()

dwf.FDwfParamSet(DwfParamOnClose, c_int(0)) # 0 = run, 1 = stop, 2 = shutdown

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

print("Configuring SPI...")
dwf.FDwfDigitalSpiFrequencySet(hdwf, c_double(1e3))
dwf.FDwfDigitalSpiClockSet(hdwf, c_int(11))
dwf.FDwfDigitalSpiDataSet(hdwf, c_int(0), c_int(0)) # 0 DQ0_MOSI_SISO = DIO-2
dwf.FDwfDigitalSpiIdleSet(hdwf, c_int(0), c_int(3)) # 0 DQ0_MOSI_SISO = DwfDigitalOutIdleZet
dwf.FDwfDigitalSpiModeSet(hdwf, c_int(0))
dwf.FDwfDigitalSpiOrderSet(hdwf, c_int(1)) # 1 MSB first

dwf.FDwfDigitalSpiSelect(hdwf, c_int(12), c_int(1)) # relay control
dwf.FDwfDigitalSpiSelect(hdwf, c_int(13), c_int(1)) 
dwf.FDwfDigitalSpiSelect(hdwf, c_int(14), c_int(1)) 

for i in range(1,11):
    dwf.FDwfDigitalSpiSelect(hdwf, c_int(i), c_int(1)) # CS: idle high

time.sleep(1)

dwf.FDwfDigitalSpiSelect(hdwf, c_int(1), c_int(0))
dwf.FDwfDigitalSpiWriteOne(hdwf, c_int(0), c_int(8), c_uint(0x01)) # write 1 byte to MOSI
dwf.FDwfDigitalSpiSelect(hdwf, c_int(1), c_int(1))

dwf.FDwfDigitalSpiSelect(hdwf, c_int(2), c_int(0))
dwf.FDwfDigitalSpiWriteOne(hdwf, c_int(0), c_int(8), c_uint(0x02)) # write 1 byte to MOSI
dwf.FDwfDigitalSpiSelect(hdwf, c_int(2), c_int(1))

dwf.FDwfDigitalSpiSelect(hdwf, c_int(3), c_int(0))
dwf.FDwfDigitalSpiWriteOne(hdwf, c_int(0), c_int(8), c_uint(0x03)) # write 1 byte to MOSI
dwf.FDwfDigitalSpiSelect(hdwf, c_int(3), c_int(1))

dwf.FDwfDeviceCloseAll()
