# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:36:16 2023

@author: Phili
"""

import cv2
import numpy as np
import time

# Define the cropping coordinates
#<<<<<<< HEAD
x1, y1 = 1104, 0
x2, y2 = 3386, 4500
for i in range(17):
    vid_run =i+1
    # Read the input video
    input_video = cv2.VideoCapture(r"D:\Focus sweep 2\run" + str(vid_run) +".mp4")
    
    # Get video properties
    width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    
    # Set up the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(r"D:\Focus sweep 2\invert sub back\run" + str(vid_run) +"crop.mp4",fourcc, fps, (x2 - x1, y2 - y1))
    fgbg = cv2.createBackgroundSubtractorMOG2()
    
    # Process the video frames
    start_time = time.time()
    while True:
        ret, frame = input_video.read()
    
        if not ret:
            break
    
        # Crop the frame
        cropped_frame = frame[y1:y2, x1:x2]
    
        # Write the cropped frame to the output video
        output_video.write(cropped_frame)
    
        #Display the cropped frame (optional)
        #cv2.imshow('Cropped Video', cropped_frame)
    
        # Exit if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    end_time = time.time()
    print("Compute time is " + str(end_time - start_time))
    
    output_video.release()
    input_video.release()
    cv2.destroyAllWindows()
    
    # Read the input video
    cap = cv2.VideoCapture(r"D:\Focus sweep 2\invert sub back\run" + str(vid_run) +"crop.mp4")
    fgbg = cv2.createBackgroundSubtractorMOG2()
    
    # Set up the output video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #cv2.namedWindow('frame',0)
    #cv2.resizeWindow('frame',300,300)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(r"D:\Focus sweep 2\invert sub back\run" + str(vid_run) +"cropsubback.mp4",fourcc, fps,(x2 - x1, y2 - y1),False)
    
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        fgmask = abs(255-fgbg.apply(frame))
        #fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
    
        #cv2.imshow('Frame', frame)
        #cv2.imshow('FG MASK Frame', fgmask)
        out.write(fgmask)
    
        keyboard = cv2.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break
    
    
    out.release()
    cap.release()
    cv2.destroyAllWindows()
#=======
x1, y1 = 1250, 1000
x2, y2 = 2400, 3000

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
start_time = time.time()
while True:
    ret, frame = input_video.read()

    if not ret:
        break

    # Crop the frame
    cropped_frame = frame[y1:y2, x1:x2]

    # Write the cropped frame to the output video
    output_video.write(cropped_frame)

    #Display the cropped frame (optional)
    #cv2.imshow('Cropped Video', cropped_frame)

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
end_time = time.time()
print("Compute time is " + str(end_time - start_time))

output_video.release()
input_video.release()
cv2.destroyAllWindows()

# Read the input video
cap = cv2.VideoCapture(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6crop and back.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2()

# Set up the output video
fps = int(cap.get(cv2.CAP_PROP_FPS))
#cv2.namedWindow('frame',0)
#cv2.resizeWindow('frame',300,300)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6croppedBW.mp4",fourcc, fps,(x2 - x1, y2 - y1),False)

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    fgmask = abs(255-fgbg.apply(frame))
    #fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

    #cv2.imshow('Frame', frame)
    #cv2.imshow('FG MASK Frame', fgmask)
    out.write(fgmask)

    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break


out.release()
cap.release()
cv2.destroyAllWindows()
#>>>>>>> c21ad30d3121bc7b212b3081bb0f1a75ed3b6eb5
