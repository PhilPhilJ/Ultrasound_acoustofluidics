"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-02-22

   Requires:                       
       Python 2.7, 3
   Description:
   Record from Scope and Play in Wavegen
"""

from dwfconstants import *
import ctypes
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

# faster connection and prevent temperature drifts
dwf.FDwfParamSet(DwfParamOnClose, c_int(1)) # 0 = run, 1 = stop, 2 = shutdown

hdwf = c_int()
print("Opening first device...")
if dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf)) != 1 or hdwf.value == 0:
    print("Failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0)) # 0 = the device will be configured only when calling FDwf###Configure

hzRate = 100e3 # 100kHz
chIn = c_int(0) # Scope 1
chOut = c_int(0) # Wavegen 1
nBufferIn = c_int()
nBufferOut = c_int()

dwf.FDwfAnalogInBufferSizeInfo(hdwf, None, byref(nBufferIn))
dwf.FDwfAnalogOutNodeDataInfo(hdwf, c_int(0), AnalogOutNodeCarrier, None, byref(nBufferOut))
nBuffer = nBufferIn.value + nBufferOut.value
rgBuffer = (c_double*nBuffer)()
print("Frequency "+str(hzRate/1000)+"kHz Delay: "+str(nBuffer/hzRate*1000)+"ms InBuff: "+str(nBufferIn.value)+" OutBuff: "+str(nBufferOut.value))

print("Start Play...")
dwf.FDwfAnalogOutNodeEnableSet(hdwf, chOut, AnalogOutNodeCarrier, c_int(1))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, chOut, AnalogOutNodeCarrier, funcPlayPattern) # do not use fractional step increments
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, chOut, AnalogOutNodeCarrier, c_double(hzRate))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, chOut, AnalogOutNodeCarrier, c_double(5.0))
dwf.FDwfAnalogOutTriggerSourceSet(hdwf, chOut, trigsrcAnalogIn)
dwf.FDwfAnalogOutWaitSet(hdwf, chOut, c_double(nBufferIn.value/hzRate))
dwf.FDwfAnalogOutConfigure(hdwf, chOut, c_int(1))

print("Start Record...")
dwf.FDwfAnalogInChannelEnableSet(hdwf, chIn, c_int(1))
dwf.FDwfAnalogInChannelRangeSet(hdwf, chIn, c_double(5.0))
dwf.FDwfAnalogInChannelOffsetSet(hdwf, chIn, c_double(0))
#dwf.FDwfAnalogInChannelAttenuationSet(hdwf, chIn, c_double(10)) # can be used to for "amplification" like +/100mV signals to +/-1
dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord)
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(hzRate))
dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double(0)) # infinite
dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))

cBuffer = 0
cFree = c_int(0)
cAvailable = c_int(0)
cLost = c_int(0)
cCorrupted = c_int(0)
sts = c_ubyte(0)


# Note: The analog-in captures samples as voltage and the analog-out expects normalized to +/-1

# loop to Record and Play data chunks
print("Press Ctrl+C to stop...")
try:
    while True :
        if dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts)) != 1: # handle error
            print("FDwfAnalogInStatus Error")
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            print(szerr.value)
            break
        
        if sts.value != DwfStateRunning.value: 
            continue
            
        dwf.FDwfAnalogInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
        if cLost.value != 0 : 
            print("Input buffer overflow")
            break
        if cCorrupted.value != 0 :
            print("Input buffer may overflow")
            break
        if cAvailable.value > 0 :
            if cBuffer + cAvailable.value > nBuffer :
                print("Software buffer overflow")
                break
            dwf.FDwfAnalogInStatusData(hdwf, chIn, byref(rgBuffer, sizeof(c_double)*cBuffer), cAvailable)
            # process new samples
            cBuffer += cAvailable.value
                
        if dwf.FDwfAnalogOutStatus(hdwf, chOut, byref(sts)) != 1: # handle error
            print("FDwfAnalogOutStatus Error")
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            print(szerr.value)
            break
        
        if sts.value != DwfStateRunning.value :
            continue
        dwf.FDwfAnalogOutNodePlayStatus(hdwf, chOut, AnalogOutNodeCarrier, byref(cFree), byref(cLost), byref(cCorrupted))
        if cLost.value != 0 : 
            print("Output buffer underflow")
            break
        if cCorrupted.value != 0 :
            print("Output buffer may underflow")
            break
        if cBuffer-cFree.value < 0 :
            print("Software buffer underflow "+str(cFree.value))
            break
        if dwf.FDwfAnalogOutNodePlayData(hdwf, chOut, AnalogOutNodeCarrier, byref(rgBuffer), cFree) != 1 : # offset for double is *8 (bytes) 
            print("Error")
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            print(szerr.value)
            break
        cBuffer -= cFree.value
        memmove(byref(rgBuffer), byref(rgBuffer, sizeof(c_double)*cFree.value), sizeof(c_double)*cBuffer)
        
except KeyboardInterrupt:
    pass

print("done")
dwf.FDwfAnalogOutReset(hdwf, chOut)
dwf.FDwfDeviceClose(hdwf)

