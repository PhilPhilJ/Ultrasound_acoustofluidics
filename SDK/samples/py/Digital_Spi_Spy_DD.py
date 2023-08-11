"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2023-02-03

   Requires:                       
       Python 2.7, 3
   Description:
   Intended to be used with Digital Discovery.
   Decodes SPI communication.
"""

from ctypes import *
from dwfconstants import *
import math
import sys
import ctypes

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

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

print("Configuring Digital In...")

nSamples = 100000
rgdwSamples = (c_uint32*nSamples)()
cAvailable = c_int()
cLost = c_int()
cCorrupted = c_int()

# 0 represents DIO-24 with order 1
idxCS = 0 # DIO-24
idxClk = 1 # DIO-25
idxMosi = 2 # DIO-26
idxMiso = 3 # DIO-27
nBits = 8

print("Configuring SPI spy...")
# record mode
dwf.FDwfDigitalInAcquisitionModeSet(hdwf, acqmodeRecord)
# for sync mode set divider to -1 
dwf.FDwfDigitalInDividerSet(hdwf, c_int(-1))
# 32bit per sample format
dwf.FDwfDigitalInSampleFormatSet(hdwf, c_int(32))
# noise samples
dwf.FDwfDigitalInSampleModeSet(hdwf, c_int(1)) 
# continuous sampling 
dwf.FDwfDigitalInTriggerPositionSet(hdwf, c_int(-1))
# in sync mode the trigger is used for sampling condition
# trigger detector mask:          low &     high    & ( rising                     | falling )
dwf.FDwfDigitalInTriggerSet(hdwf, c_int(0), c_int(0), c_int((1<<idxClk)|(1<<idxCS)), c_int(0))
# sample on clock rising edge for sampling bits, or CS rising edge to detect frames

# for Digital Discovery bit order: DIO24:39; with 32 bit sampling [DIO24:39 + DIN0:15]
dwf.FDwfDigitalInInputOrderSet(hdwf, c_int(1))

dwf.FDwfDigitalInConfigure(hdwf, c_int(0), c_int(1))

try:
    fsMosi = 0
    fsMiso = 0
    cBit = 0
    rgMosi = []
    rgMiso = []
    while True:
        
        dwf.FDwfDigitalInStatus(hdwf, c_int(1), byref(sts))
        dwf.FDwfDigitalInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))

        if cLost.value :
            print("Samples were lost!")
        if cCorrupted.value :
            print("Samples could be corrupted!")
        if cAvailable.value > nSamples :
            cAvailable = c_int(nSamples)
        
        dwf.FDwfDigitalInStatusData(hdwf, rgdwSamples, c_int(cAvailable.value*4)) # 32bit data
        
        for i in range(cAvailable.value):
            v = rgdwSamples[i]
            if (v>>idxCS)&1: # CS high, inactive, print data
                if len(rgMosi) != 0 :
                    print("MOSI:", end=" ")
                    for j in range(len(rgMosi)) :
                        print("h%02X," % rgMosi[j], end=" ")
                    print("")
                if len(rgMiso) != 0 :
                    print("MISO:", end=" ")
                    for j in range(len(rgMiso)) :
                        print("h%02X," % rgMiso[j], end=" ")
                    print("")
                if cBit != 0: # log leftover bits, frame not multiple of nBits
                    print("leftover bits %d : h%02X | h%02X" % (cBit, fsMosi, fsMiso))
                cBit = 0
                fsMosi = 0
                fsMiso = 0
                rgMosi.clear()
                rgMiso.clear()
            else:
                cBit+=1
                fsMosi <<= 1 # MSB first
                fsMiso <<= 1 # MSB first
                if (v>>idxMosi)&1 :
                    fsMosi |= 1
                if (v>>idxMiso)&1 :
                    fsMiso |= 1
                if cBit >= nBits: # got nBits of bits
                    rgMosi.append(fsMosi)
                    rgMiso.append(fsMiso)
                    cBit = 0
                    fsMosi = 0
                    fsMiso = 0
except KeyboardInterrupt:
    pass

dwf.FDwfDeviceClose(hdwf)
