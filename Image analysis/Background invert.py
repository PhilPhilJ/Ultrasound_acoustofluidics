# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:36:16 2023

@author: Phili
"""

import cv2
import numpy as np
import time

# Define the cropping coordinates
x1, y1 = 1104, 0
x2, y2 = 3386, 4504

# Read the input video
input_video = cv2.VideoCapture(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_5.mp4")

# Get video properties
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(input_video.get(cv2.CAP_PROP_FPS))

# Set up the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6crop and back.mp4",fourcc, fps, (x2 - x1, y2 - y1))
fgbg = cv2.createBackgroundSubtractorMOG2()

# Process the video frames
while True:
    ret, frame = input_video.read()
    if not ret:
        break

    # Crop the frame
    cropped_frame = frame[y1:y2, x1:x2]

    # Write the cropped frame to the output video
    output_video.write(cropped_frame)

output_video.release()
input_video.release()
# Read the input video
cap = cv2.VideoCapture(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6crop and back.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2()

# Set up the output video
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6croppedBW.mp4",fourcc, fps,(x2 - x1, y2 - y1),False)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    fgmask = abs(255-fgbg.apply(frame))

    out.write(fgmask)

    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

out.release()
cap.release()