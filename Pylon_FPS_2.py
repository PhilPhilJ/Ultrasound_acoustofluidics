#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 12:32:47 2023

@author: joakimpihl
"""

from pypylon import pylon
import numpy as np
import time
import cv2
from frameCut import *

#Connects to the camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

######################## Grabbing strategy ########################
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Grabing Continusely (video) with minimal delay
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

size = (4504, 4504) # Camera resoloution: 4504x4504px, FPS: 18
FPS = 18 # Frames per second of camera
fourcc = cv2.VideoWriter_fourcc(*'mp4v') #Defines output format, mp4
out = cv2.VideoWriter('C:/Users/s102772/Desktop/Algae_Vid_Exp.mp4', fourcc, FPS, size) #Defines a path to where the movie is saved, video format, playback framerate, and video size/resolution

delta_t = 10 #How long should the recording be, measured in seconds

if 'start' in globals():
    del start
while camera.IsGrabbing():
      grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
      if grabResult.GrabSucceeded():
          # Access the image data
          image = converter.Convert(grabResult)
          img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
          if not 'IL' in globals() and not 'IR' in globals():
              IL,IR = frameCut(img)
          img = img[:,IL:IR]
          stop = time.time() 
                
          cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
          cv2.imshow('Algae experiment', img)

      if not 'start' in globals(): #If the variable start doesn't exist define a start time and start recording
          start = time.time()
          print('Start timing')
      elif stop-start>=delta_t: #Stop recording when delta_t seconds has elapsed  
          print('Stop timing')
          print('Stop-start= ' + str(stop-start) + ' s')
          break
      
      if 'start' in globals() and stop-start<delta_t:
          out.write(img)

      grabResult.Release()

cv2.destroyAllWindows()      
out.release() 
camera.StopGrabbing()


# This part loads the video that the script created and computes a framerate (FPS) based on the movie
# =============================================================================
# vid = cv2.VideoCapture('C:/Users/s102772/Desktop/Algae_Vid_Exp.mp4') #Loads the video
# 
# n_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
# FPS = round(n_frames/(stop-start),2)
# 
# print('FPS: ' + str(FPS))
# =============================================================================










