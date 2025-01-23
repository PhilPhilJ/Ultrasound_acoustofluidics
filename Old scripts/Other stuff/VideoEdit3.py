#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 13:49:01 2023

@author: joakimpihl
"""

import cv2
import numpy as np
import pandas as pd


def process_video(input_path, output_path, path_imp_times, path_times):
    vid = cv2.VideoCapture(input_path)
    imp_times = pd.read_csv(path_imp_times, delimiter=';', encoding='utf-8') # [0] = focus start, [1] = focus stop
    timestamps = pd.read_csv(path_times, delimiter=';', encoding='utf-8') # Timestamps start at index 2
    
    # Manipulate csv files - Timescaling, and retrieve frequency information
    timestamps, imp_times = timestamps['Frame time'].tolist(), np.array(imp_times['Important times'].tolist())
    timestamps = np.array(timestamps[2:len(timestamps)])
    imp_times = np.array([imp_times[1], imp_times[2]])
    t_index_0 = np.where(np.isclose(timestamps, imp_times[0], atol=0.1, rtol=0)) #Frame where focusing is started
    if len(t_index_0) == 1:
        t_index_0 = int(t_index_0[0])
    else:
        print('Error! Multiple starting indeces were found.')
    timestamps, imp_times = timestamps-timestamps[t_index_0], imp_times-timestamps[t_index_0]
    
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS = vid.get(cv2.CAP_PROP_FPS)
    output_size = (int(3387 - 1104), height)

    fourcc = cv2.VideoWriter_fourcc(*'H264')  # Use 'H264' codec
  # Use 'MJPG' codec
    out = cv2.VideoWriter(output_path, fourcc, FPS, output_size)
    
    background_frames = np.empty((t_index_0, height, int(3387-1104)))


    for i in range(0, t_index_0):
        ret, frame = vid.read()
        if not ret:
            break
        # Convert to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Crop the width
        frame_gray_cropped = frame_gray[:, 1104:3387]
        # Assign to background_frames
        background_frames[i] = frame_gray_cropped
        print(f"Processed frame {i}/{t_index_0}")

    
    vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
    mean_background = np.mean(background_frames, axis=0)

    for i in range(total_frames):
        ret, frame = vid.read()
        if not ret:
            break
    
        # Convert to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Crop the width
        frame_gray_cropped = frame_gray[:, 1104:3387]
    
        frame_no_bg_gray_cropped = frame_gray_cropped - mean_background
    
        # Convert to uint8
        frame_no_bg_gray_cropped = frame_no_bg_gray_cropped.astype(np.uint8)
    
        # Write the processed frame
        out.write(frame_no_bg_gray_cropped)
        print(f"Processed frame {i}/{total_frames}")


    # Release resources
    vid.release()
    out.release()
    cv2.destroyAllWindows()



# Paths to files
vid_num = 8 #Video 0 through 16
# Example usage:
input_path = '/Users/joakimpihl/Desktop/Focus sweep 2/run'+str(vid_num)+'.mp4'
output_path = '/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep 2.1 sub back/run'+str(vid_num)+'.mp4'
path_imp_times = '/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep 2 sub back/Important times/Important times'+str(vid_num)+'.csv'
path_times = '/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep 2 sub back/Timestamps/Time Stamps'+str(vid_num)+'.csv'

process_video(input_path, output_path, path_imp_times, path_times)
