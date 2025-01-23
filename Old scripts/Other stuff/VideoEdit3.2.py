#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 15:21:40 2023

@author: joakimpihl
"""

import cv2
import numpy as np
import pandas as pd


# Paths to files
vid_num = 0 #Video 0 through 15
# Example usage:
background_path = '/Users/joakimpihl/Desktop/Videos/Focus sweep 4/Background/Background.mp4'
input_path = '/Users/joakimpihl/Desktop/Videos/Focus sweep 4/run'+str(vid_num)+'.mp4'
output_path = '/Users/joakimpihl/Desktop/Videos/4 - no background/run'+str(vid_num)+'.mp4'
path_imp_times = '/Users/joakimpihl/Desktop/Videos/Focus sweep 4/Important times'+str(vid_num)+'.csv'
path_times = '/Users/joakimpihl/Desktop/Videos/Focus sweep 4/Time Stamps'+str(vid_num)+'.csv'


vid = cv2.VideoCapture(input_path)
background = cv2.VideoCapture(background_path)
imp_times = pd.read_csv(path_imp_times, delimiter=';', encoding='utf-8')['Important times'].tolist() # [0] = focus start, [1] = focus stop
timestamps = pd.read_csv(path_times, delimiter=';', encoding='utf-8')['Frame time'].iloc[2:].tolist() # Timestamps start at index 2
  
# Manipulate csv files - Timescaling, and retrieve frequency information
t_index_0 = None
for i, ts in enumerate(timestamps):
    if np.isclose(ts, imp_times[1], atol=0.01, rtol=0):
        if t_index_0 is None:
            t_index_0 = i
        else:
            raise ValueError('Error! Multiple starting indices were found.')

if t_index_0 is not None:
    timestamps = np.array(timestamps) - timestamps[t_index_0]
    imp_times = np.array(imp_times) - timestamps[t_index_0]
else:
    raise ValueError('Error! No starting index found.')
  
total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
total_frames_background = int(background.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = vid.get(cv2.CAP_PROP_FPS)
output_size = (int(1184 - 159), height)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Use 'H264' codec
# Use 'MJPG' codec
out = cv2.VideoWriter(output_path, fourcc, FPS, output_size)
  
background_frames = np.empty((total_frames_background, height, int(1184 - 159)))


for i in range(total_frames_background):
    ret, frame = background.read()
    if not ret:
        break
    # Convert to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Crop the width
    frame_gray_cropped = frame_gray[:, 216:1255]
    # Assign to background_frames
    background_frames[i] = frame_gray_cropped
    print(f"Processed frame {i}/{total_frames_background}")

  
mean_background = np.mean(background_frames, axis=0)
#%%
for i in range(total_frames):
    ret, frame = vid.read()
    if not ret:
        break
  
    # Convert to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
    # Crop the width
    frame_gray_cropped = frame_gray[:, 216:1255]
  
    frame_no_bg_gray_cropped = frame_gray_cropped - mean_background
  
    # Convert to uint8
    frame_no_bg_gray_cropped = frame_no_bg_gray_cropped.astype(np.uint8)
    
    #Make the video binary
    frame_no_bg_gray_cropped_binary = cv2.adaptiveThreshold(frame_no_bg_gray_cropped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    frame_no_bg_gray_cropped_binary = 255-frame_no_bg_gray_cropped_binary
  
    # Write the processed frame
    out.write(frame_no_bg_gray_cropped_binary)
    print(f"Processed frame {i}/{total_frames}")


# Release resources
vid.release()
out.release()
cv2.destroyAllWindows()