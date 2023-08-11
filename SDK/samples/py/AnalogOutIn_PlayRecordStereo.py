"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2021-05-03

   Requires:                       
       Python 2.7, 3
   Description:
   Play stereo WAV file on Wavegen channels
   Record to stereo WAV file Scope channels
"""

from dwfconstants import *
import ctypes
import sys
from scipy.io import wavfile
import numpy


print("Load stereo.wav file")
rate, data_raw = wavfile.read("stereo.wav")
length = data_raw.shape[0]
slength = 1.0*length/rate

print("Rate: "+str(rate))
print("Type:"+str(data_raw.dtype))
print("Channels:"+str(data_raw.shape[1]))
print("Length: "+str(length)+" "+str(slength)+"s")
if data_raw.shape[1] != 2:
    print("Expecting stereo WAV file")
    exit

data_float0 = numpy.fromiter(data_raw[:, 0], dtype = numpy.float64)
data_float1 = numpy.fromiter(data_raw[:, 1], dtype = numpy.float64)

# AnalogOut expects double normalized to +/-1 value
if data_raw.dtype == numpy.uint8 :
    data_float0 /= 128.0
    data_float0 -= 1.0
    data_float1 /= 128.0
    data_float1 -= 1.0
elif data_raw.dtype == numpy.int16 :
    data_float0 /= 32768.0
    data_float1 /= 32768.0
elif data_raw.dtype == numpy.int32 :
    data_float0 /= 2147483648.0
    data_float1 /= 2147483648.0
    
data0 = (ctypes.c_double * length)(*data_float0)
data1 = (ctypes.c_double * length)(*data_float1)


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

hdwf = c_int()
print("Opening first device...")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    print("Failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()


print("Staring record...")
iRecord = 0
record0 = (c_int16*length)()
record1 = (c_int16*length)()
#set up acquisition
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_int(1)) # channel 1
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_int(1)) # channel 2
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(2.0))
dwf.FDwfAnalogInChannelOffsetSet(hdwf, c_int(-1), c_double(0))
dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord)
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(rate))
dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double(slength))
dwf.FDwfAnalogInTriggerPositionSet(hdwf, c_double(0))
dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcAnalogOut1)
dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))


print("Playing audio...")
iPlay = 0
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(0), c_int(1)) # Wavegen channel 1
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(1), c_int(0), c_int(1)) # Wavegen channel 2
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(-1), c_int(0), funcPlay)
dwf.FDwfAnalogOutRepeatSet(hdwf, c_int(-1), c_int(1))
dwf.FDwfAnalogOutRunSet(hdwf, c_int(-1), c_double(slength))
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(-1), c_int(0), c_double(rate))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(-1), c_int(0), c_double(2.0))

# prime the buffer with the first chunk of data
cBuffer = c_int(0)
dwf.FDwfAnalogOutNodeDataInfo(hdwf, c_int(0), c_int(0), c_int(0), byref(cBuffer))
if cBuffer.value > length : cBuffer.value = length
dwf.FDwfAnalogOutNodeDataSet(hdwf, c_int(0), c_int(0), data0, cBuffer)
dwf.FDwfAnalogOutNodeDataSet(hdwf, c_int(1), c_int(0), data1, cBuffer)
iPlay += cBuffer.value

dwf.FDwfAnalogOutConfigure(hdwf, c_int(-1), c_int(1))

dataLost = c_int(0)
dataFree = c_int(0)
dataAvailable = c_int(0)
dataCorrupt = c_int(0)
sts = c_ubyte(0)
totalLost = 0
totalCorrupt = 0

# loop to send out and read in data chunks
while iRecord < length :
    if dwf.FDwfAnalogOutStatus(hdwf, c_int(0), byref(sts)) != 1: # handle error
        print("Error")
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(szerr.value)
        break
    
    # play, analog out data chunk
    if sts.value == DwfStateRunning.value and iPlay < length :  # running and more data to stream
        dwf.FDwfAnalogOutNodePlayStatus(hdwf, c_int(0), c_int(0), byref(dataFree), byref(dataLost), byref(dataCorrupt))
        totalLost += dataLost.value
        totalCorrupt += dataCorrupt.value
        if iPlay + dataFree.value > length : # last chunk might be less than the free buffer size
            dataFree.value = length - iPlay
        if dataFree.value > 0 : 
            if dwf.FDwfAnalogOutNodePlayData(hdwf, c_int(0), c_int(0), byref(data0, iPlay*8), dataFree) != 1: # offset for double is *8 (bytes) 
                print("Error")
                break
            if dwf.FDwfAnalogOutNodePlayData(hdwf, c_int(1), c_int(0), byref(data1, iPlay*8), dataFree) != 1:
                print("Error")
                break
            iPlay += dataFree.value
    
    if dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts)) != 1: # handle error
        print("Error")
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(szerr.value)
        break
    
    # record, analog in data chunk
    if sts.value == DwfStateRunning.value or sts.value == DwfStateDone.value : # recording or done
        dwf.FDwfAnalogInStatusRecord(hdwf, byref(dataAvailable), byref(dataLost), byref(dataCorrupt))
        iRecord += dataLost.value
        totalLost += dataLost.value
        totalCorrupt += dataCorrupt.value
        if dataAvailable.value > 0 :
            if iRecord+dataAvailable.value > length :
                dataAvailable = c_int(length-iRecord)
            # get Scope channel 1 data chunk, offset for 16bit data is 2*
            dwf.FDwfAnalogInStatusData16(hdwf, c_int(0), byref(record0, 2*iRecord), c_int(0), dataAvailable) 
            # get Scope channel 2 data chunk
            dwf.FDwfAnalogInStatusData16(hdwf, c_int(1), byref(record1, 2*iRecord), c_int(0), dataAvailable)
            iRecord += dataAvailable.value


print("Lost: "+str(totalLost))
print("Corrupt: "+str(totalCorrupt))
print("done")
dwf.FDwfAnalogOutReset(hdwf, c_int(-1))
dwf.FDwfDeviceClose(hdwf)


print("Writing record.wav file");
wavfile.write('record.wav', rate, numpy.stack((record0, record1)).T)
print("done")
