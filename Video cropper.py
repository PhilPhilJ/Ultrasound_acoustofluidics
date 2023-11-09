# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:15:11 2023

@author: Phili
"""

import cv2
import numpy as np

# Define the cropping coordinates
x1, y1 = 1250, 1000
x2, y2 = 2400, 3000

# Read the input video
input_video = cv2.VideoCapture(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6.mp4")

# Get video properties
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(input_video.get(cv2.CAP_PROP_FPS))

# Set up the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6cropped.mp4",fourcc, fps, (x2 - x1, y2 - y1))

# Process the video frames
while True:
    ret, frame = input_video.read()

    if not ret:
        break

    # Crop the frame
    cropped_frame = frame[y1:y2, x1:x2]

    # Write the cropped frame to the output video
    output_video.write(cropped_frame)

    # Display the cropped frame (optional)
    cv2.imshow('Cropped Video', cropped_frame)

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the input and output videos and close the display window
input_video.release()
output_video.release()
cv2.destroyAllWindows()