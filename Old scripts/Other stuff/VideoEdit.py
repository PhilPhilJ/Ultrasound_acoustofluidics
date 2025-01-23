#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 17:59:28 2023

@author: joakimpihl
"""

import cv2
import numpy as np

vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Focus sweep/run4.mp4')
n_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = vid.get(cv2.CAP_PROP_FPS)
size = (int(3387-1104), height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/Users/joakimpihl/Desktop/test.mp4', fourcc, FPS, size)

frames = np.empty((n_frames, height, int(3387-1104)), dtype=int)

for i in range(n_frames):
    ret, frame = vid.read()
    img = np.array(frame)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    img = img[:, 1104:3387]
    frames[i] = img
    print(i)

vid.release()
#Write the video
for i in range(n_frames):
    out.write(frames[i])

out.release()    
vid.release()
