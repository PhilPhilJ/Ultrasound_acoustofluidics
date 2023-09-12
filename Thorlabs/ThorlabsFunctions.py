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

###############################################################################
### functions for X direction

def PositionX():
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")
    
    lib.TLI_InitializeSimulations()
    
    scale_fc = 34304
    
    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27258278")

    lib.SCC_Open(serialNumber)
    lib.SCC_StartPolling(serialNumber, c_int(100))
    lib.SCC_EnableChannel(serialNumber)
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)
    position = lib.SCC_GetPositionCounter(serialNumber)
    position = position / scale_fc 
    
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return position

def MoveRelX(distance=1):
    """
    input the desired distance in mm you want Thorlabs to move.

    Parameters
    ----------
    distance : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    None.

    """
    scale_fc = 34304
    distance_mm = round(distance * scale_fc)
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27258278")

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
    time.sleep(abs(distance) + 1)
    position = lib.SCC_GetPositionCounter(serialNumber)
    print("Thorlabs moved " + str(distance) + "mm in the x direction and is now at " + str(round(position/scale_fc , 2)) + "mm")
    
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return

def MoveAbsX(position = 1):
    """
    input the position in mm you want to move Thorlabs to.

    Parameters
    ----------
    position : TYPE, optional
        DESCRIPTION. The default is 1.
    times : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    position_mm : TYPE
        DESCRIPTION.

    """
    
    scale_fc = 34304
    position_mm = round(position * scale_fc)
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27258278")

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

    lib.SCC_SetMoveAbsolutePosition(serialNumber, c_int(position_mm))
    current_position = lib.SCC_GetPositionCounter(serialNumber)
    time.sleep(1)
    lib.SCC_MoveAbsolute(serialNumber)
    print("Moving...")
    
    time.sleep(abs(position - current_position//scale_fc) + 1)
    
    current_position = lib.SCC_GetPositionCounter(serialNumber)
    print("Thorlabs moved to " + str(round(current_position/scale_fc , 2)) + "mm")

    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return

def HomeX():
    """
    Simply homes Thorlabs. No input.

    Returns
    -------
    None.

    """
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27258278")

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

def CheckHomeX():
    """
    Checks if Thorlabs is homed.

    Returns
    -------
    homed : TYPE
        DESCRIPTION.
        
        Returns either:
            homed = True
            homed = False
    """
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27258278")

    lib.SCC_Open(serialNumber)
    lib.SCC_StartPolling(serialNumber, c_int(100))
    lib.SCC_EnableChannel(serialNumber)
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_LoadSettings(serialNumber)
    time.sleep(0.5)
    position = lib.SCC_GetPositionCounter(serialNumber)
    if position == 0:
        homed = True
    else:
        homed = False

    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    lib.TLI_UninitializeSimulations()
    
    return homed

###############################################################################
### functions for Y direction


def PositionY():
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")
    
    lib.TLI_InitializeSimulations()
    
    scale_fc = 34304
    
    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259679")

    lib.SCC_Open(serialNumber)
    lib.SCC_StartPolling(serialNumber, c_int(100))
    lib.SCC_EnableChannel(serialNumber)
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)
    position = lib.SCC_GetPositionCounter(serialNumber)
    position = position / scale_fc 
    
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return position

def MoveRelY(distance=1):
    """
    input the desired distance in mm you want Thorlabs to move.

    Parameters
    ----------
    distance : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    None.

    """
    scale_fc = 34304
    distance_mm = round(distance * scale_fc)
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259679")

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
    time.sleep(abs(distance) + 1)
    position = lib.SCC_GetPositionCounter(serialNumber)
    print("Thorlabs moved " + str(distance) + "mm in the x direction and is now at " + str(round(position/scale_fc , 2)) + "mm")
    
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return

def MoveAbsY(position = 1):
    """
    input the position in mm you want to move Thorlabs to.

    Parameters
    ----------
    position : TYPE, optional
        DESCRIPTION. The default is 1.
    times : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    position_mm : TYPE
        DESCRIPTION.

    """
    
    scale_fc = 34304
    position_mm = round(position * scale_fc)
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259679")

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

    lib.SCC_SetMoveAbsolutePosition(serialNumber, c_int(position_mm))
    current_position = lib.SCC_GetPositionCounter(serialNumber)
    time.sleep(1)
    lib.SCC_MoveAbsolute(serialNumber)
    print("Moving...")
    
    time.sleep(abs(position - current_position//scale_fc) + 1)
    
    current_position = lib.SCC_GetPositionCounter(serialNumber)
    print("Thorlabs moved to " + str(round(current_position/scale_fc , 2)) + "mm")

    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return

def HomeY():
    """
    Simply homes Thorlabs. No input.

    Returns
    -------
    None.

    """
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259679")

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

def CheckHomeY():
    """
    Checks if Thorlabs is homed.

    Returns
    -------
    homed : TYPE
        DESCRIPTION.
        
        Returns either:
            homed = True
            homed = False
    """
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259679")

    lib.SCC_Open(serialNumber)
    lib.SCC_StartPolling(serialNumber, c_int(100))
    lib.SCC_EnableChannel(serialNumber)
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_LoadSettings(serialNumber)
    time.sleep(0.5)
    position = lib.SCC_GetPositionCounter(serialNumber)
    if position == 0:
        homed = True
    else:
        homed = False

    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    lib.TLI_UninitializeSimulations()
    
    return homed

###############################################################################
### functions for z direction

def PositionZ():
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")
    
    lib.TLI_InitializeSimulations()
    
    scale_fc = 34304
    
    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259728")

    lib.SCC_Open(serialNumber)
    lib.SCC_StartPolling(serialNumber, c_int(100))
    lib.SCC_EnableChannel(serialNumber)
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)
    position = lib.SCC_GetPositionCounter(serialNumber)
    position = position / scale_fc 
    
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return position

def MoveRelZ(distance=1):
    """
    input the desired distance in mm you want Thorlabs to move.

    Parameters
    ----------
    distance : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    None.

    """
    scale_fc = 34304
    distance_mm = round(distance * scale_fc)
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259728")

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
    time.sleep(abs(distance) + 1)
    position = lib.SCC_GetPositionCounter(serialNumber)
    print("Thorlabs moved " + str(distance) + "mm in the x direction and is now at " + str(round(position/scale_fc , 2)) + "mm")
    
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return

def MoveAbsZ(position = 1):
    """
    input the position in mm you want to move Thorlabs to.

    Parameters
    ----------
    position : TYPE, optional
        DESCRIPTION. The default is 1.
    times : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    position_mm : TYPE
        DESCRIPTION.

    """
    
    scale_fc = 34304
    position_mm = round(position * scale_fc)
    
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259728")

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

    lib.SCC_SetMoveAbsolutePosition(serialNumber, c_int(position_mm))
    current_position = lib.SCC_GetPositionCounter(serialNumber)
    time.sleep(1)
    lib.SCC_MoveAbsolute(serialNumber)
    print("Moving...")
    
    time.sleep(abs(position - current_position//scale_fc) + 1)
    
    current_position = lib.SCC_GetPositionCounter(serialNumber)
    print("Thorlabs moved to " + str(round(current_position/scale_fc , 2)) + "mm")

    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    return

def HomeZ():
    """
    Simply homes Thorlabs. No input.

    Returns
    -------
    None.

    """
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259728")

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

def CheckHomeZ():
    """
    Checks if Thorlabs is homed.

    Returns
    -------
    homed : TYPE
        DESCRIPTION.
        
        Returns either:
            homed = True
            homed = False
    """
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumber = c_char_p(b"27259728")

    lib.SCC_Open(serialNumber)
    lib.SCC_StartPolling(serialNumber, c_int(100))
    lib.SCC_EnableChannel(serialNumber)
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_LoadSettings(serialNumber)
    time.sleep(0.5)
    position = lib.SCC_GetPositionCounter(serialNumber)
    if position == 0:
        homed = True
    else:
        homed = False

    lib.SCC_ClearMessageQueue(serialNumber)
    lib.SCC_StopPolling(serialNumber)
    lib.SCC_Close(serialNumber)
    
    lib.TLI_UninitializeSimulations()
    
    return homed

###############################################################################
### Functions for all directions

def HomeAll():
    """
    Simply homes Thorlabs. No input.

    Returns
    -------
    None.

    """
    if sys.version_info < (3, 8):
        os.chdir(r"C:\Program Files\Thorlabs\Kinesis")
    else:
        os.add_dll_directory(r"C:\Program Files\Thorlabs\Kinesis")
    lib = cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

    lib.TLI_InitializeSimulations()

    lib.TLI_BuildDeviceList()
    serialNumberX = c_char_p(b"27258278")
    serialNumberY = c_char_p(b"27259679")
    serialNumberZ = c_char_p(b"27259728")

    lib.SCC_Open(serialNumberX)
    lib.SCC_Open(serialNumberY)
    lib.SCC_Open(serialNumberZ)
    lib.SCC_StartPolling(serialNumberX, c_int(100))
    lib.SCC_StartPolling(serialNumberY, c_int(100))
    lib.SCC_StartPolling(serialNumberZ, c_int(100))
    lib.SCC_EnableChannel(serialNumberX)
    lib.SCC_EnableChannel(serialNumberY)
    lib.SCC_EnableChannel(serialNumberZ)
    time.sleep(1)
    lib.SCC_ClearMessageQueue(serialNumberX)
    lib.SCC_ClearMessageQueue(serialNumberY)
    lib.SCC_ClearMessageQueue(serialNumberZ)
    
    homed = False
    if homed == False:
        print("Homing Device...")
        homeStartTime = time.time()
        lib.SCC_Home(serialNumberX)
        lib.SCC_Home(serialNumberY)
        lib.SCC_Home(serialNumberZ)
        messageType = c_ushort()
        messageID = c_ushort()
        messageData = c_ulong()
        while messageID.value != 0 or messageType.value != 2:
            lib.SCC_WaitForMessage(serialNumberX, byref(messageType), byref(messageID), byref(messageData))
        while messageID.value != 0 or messageType.value != 2:
            lib.SCC_WaitForMessage(serialNumberY, byref(messageType), byref(messageID), byref(messageData))
        while messageID.value != 0 or messageType.value != 2:
            lib.SCC_WaitForMessage(serialNumberZ, byref(messageType), byref(messageID), byref(messageData))
    
        print("Homed!")