#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 12:32:47 2023

@author: joakimpihl
"""

from pypylon import pylon
import numpy as np
import time
import random
import cv2

if not 'camera' in globals():
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

#%%
# The parameter MaxNumBuffer can be used to control the count of buffers
# allocated for grabbing. The default value of this parameter is 10.
camera.MaxNumBuffer = 30


######################## Grabbing strategy ########################

# The GrabStrategy_OneByOne strategy is used. The images are processed
# in the order of their arrival.
#camera.StartGrabbing(pylon.GrabStrategy_OneByOne)



# The GrabStrategy_LatestImageOnly strategy is used. The images are processed
# in the order of their arrival but only the last received image
# is kept in the output queue.
# This strategy can be useful when the acquired images are only displayed on the screen.
# If the processor has been busy for a while and images could not be displayed automatically
# the latest image is displayed when processing time is available again.
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

######################## Grabbing strategy ########################


# Grabing Continusely (video) with minimal delay
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

#cap = cv2.VideoCapture(0) #VideoCapture object which stores the frames, the argument is just the device index (may be 0, or -1)
size = (4504, 4504) # Camera resoloution: 4504x4504px, FPS: 18
FPS = 18 # Frames per second of camera
fourcc = cv2.VideoWriter_fourcc(*'mp4v') #Defines output format, mp4
out = cv2.VideoWriter('C:/Users/s102772/Desktop/Algae_Vid_Exp.mp4', fourcc, FPS, size) #Change path to saved location

delta_t = 10 #How long should the recording be
runs = 10
fps = np.zeros(runs) 

for i in range(runs):
    if i <= runs:
        if 'start' in globals():
            del start
        while camera.IsGrabbing():
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabResult)
                img = image.GetArray() # Array of size (4504, 4504, 3) = (pixel, pixel, rgb)
                stop = time.time()
                
                #cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Converts img to gray-scale
                cv2.namedWindow('Algae experiment', cv2.WINDOW_NORMAL)
                cv2.imshow('Algae experiment', img)
                
                if not 'start' in globals(): #If the variable start doesn't exist define a start time and record
                    start = time.time()
                    print('Starting timing')
                elif stop-start>=delta_t: #Stop recording   
                    print('Stop timing')
                    print('Stop-start= ' + str(stop-start) + ' s')
                    break
                if 'start' in globals() and stop-start<delta_t:
                    out.write(img)
                    
        out.release()          
        vid = cv2.VideoCapture('C:/Users/s102772/Desktop/Algae_Vid_Exp.mp4') #Loads the video

        n_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
        fps[i] = n_frames/(stop-start)        
                
        grabResult.Release()
    
    else:
        grabResult.Release()
        # Releasing the resource   
        out.release() 
        camera.StopGrabbing()

#%%
vid = cv2.VideoCapture('C:/Users/s102772/Desktop/Algae_Vid_Exp.mp4') #Loads the video

n_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
FPS = round(np.mean(fps),2)

print('mean FPS: ' + str(FPS))
print('sd: ' + str(round(np.std(fps),2)))









