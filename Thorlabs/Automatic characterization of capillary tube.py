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
from decimal import Decimal


def MoveRel(distance=1):
    """
    

    Parameters
    ----------
    distance : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    None.

    """
    scale_fc = 34304
    distance_mm = distance * scale_fc
    
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
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)
    
    lib.SCC_SetMotorParamsExt(serialNumber, c_double(stepsPerRev), c_double(gearBoxRatio), c_double(pitch))
    lib.SCC_LoadSettings(serialNumber)

    time.sleep(0.5)
    lib.SCC_MoveRelative(serialNumber, distance_mm)
    print("Moving...")
    time.sleep(abs(distance_mm / 20000))
    position = lib.SCC_GetPositionCounter(serialNumber)
    print("Thorlabs moved " + str(distance) + "mm in the x direction and is now at " + str(round(position/scale_fc , 2)))
    
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    lib.TLI_UninitializeSimulations()
    
    return

def MoveAbs(position = 1, times = 1):
    
    
    scale_fc = 34304
    position_mm = position * scale_fc
    
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
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)

    lib.SCC_SetMotorParamsExt(serialNumber, c_double(stepsPerRev), c_double(gearBoxRatio), c_double(pitch))
    lib.SCC_LoadSettings(serialNumber)
    
    for n in range(times):

        lib.SCC_SetMoveAbsolutePosition(serialNumber, c_int(position_mm * (n+1)))
        time.sleep(0.25)
        lib.SCC_MoveAbsolute(serialNumber)
        print("Moving...")
    
        time.sleep((n+2))
        
        position = lib.SCC_GetPositionCounter(serialNumber)
        print("Thorlabs moved to " + str(round(position/scale_fc , 2)))

    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    lib.TLI_UninitializeSimulations()
    
    return position_mm

def home():
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27258278")
    moveTimeout = 60.0

    lib.SCC_Open(serialNumber)
    lib.SCC_StartPolling(serialNumber, c_int(100))
    lib.SCC_EnableChannel(serialNumber)
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)
    
    homed = False
    if homed == False:
        print("Homing Device...")
        homeStartTime = time.time()
        lib.SCC_Home(serialNumber)
        messageType = c_ushort()
        messageID = c_ushort()
        messageData = c_ulong()
        while messageID.value != 0 or messageType.value != 2:
            lib.SCC_WaitForMessage(serialNumber, byref(messageType), byref(messageID), byref(messageData))
    
        print("Homed!")
