# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 09:05:31 2023

@author: Phili
"""

import os
import time
import ctypes
import sys
from ctypes import *

def Characterize(distance):

    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27258278")
    moveTimeout = 60.0

    stepsPerRev = 200
    gearBoxRatio = 1
    pitch = 1

    lib.SCC_Open(serialNumber)
    lib.SCC_StartPolling(serialNumber, c_int(100))
    lib.SCC_EnableChannel(serialNumber)
    time.sleep(3)
    lib.SCC_ClearMessageQueue(serialNumber)

    lib.SCC_SetMotorParamsExt(serialNumber, c_double(stepsPerRev), c_double(gearBoxRatio), c_double(pitch))
    lib.SCC_GetPositionCounter(serialNumber)
    deviceUnit = c_int(lib.SCC_GetPositionCounter(serialNumber))
    realUnit = c_double()
    lib.SCC_GetRealValueFromDeviceUnit(serialNumber, deviceUnit, byref(realUnit), 0)
    print(realUnit)
    print(deviceUnit)
    
    lib.SCC_ClearMessageQueue(serialNumber)

    lib.SCC_SetMotorParamsExt(serialNumber, c_double(stepsPerRev), c_double(gearBoxRatio), c_double(pitch))
    lib.SCC_LoadSettings(serialNumber)


    lib.SCC_GetPositionCounter(serialNumber)
    deviceUnit = c_int(lib.SCC_GetPositionCounter(serialNumber))
    realUnit = c_double()
    lib.SCC_GetRealValueFromDeviceUnit(serialNumber, deviceUnit, byref(realUnit), 0)
    print(realUnit)
    print(deviceUnit)
    print(lib.SCC_GetPositionCounter(serialNumber))


    time.sleep(5)
    lib.SCC_MoveRelative(serialNumber, distance)
    print("Moving")
    time.sleep(5)
    lib.SCC_GetPositionCounter(serialNumber)
    deviceUnit = c_int(lib.SCC_GetPositionCounter(serialNumber))
    realUnit = c_double()
    lib.SCC_GetRealValueFromDeviceUnit(serialNumber, deviceUnit, byref(realUnit), 0)
    print(realUnit)
    print(deviceUnit)


    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    print("The program has ended")

    lib.TLI_UninitializeSimulations()
    
    return