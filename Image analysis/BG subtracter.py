# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 16:58:54 2023

@author: Phili
"""

import numpy as np
import cv2 as cv

# Read the input video
cap = cv.VideoCapture(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6cropped.mp4")


fgbg = cv.createBackgroundSubtractorMOG2()

x1, y1 = 1250, 1000
x2, y2 = 2400, 3000

# Set up the output video
fps = int(cap.get(cv.CAP_PROP_FPS))
cv.namedWindow('frame',0)
cv.resizeWindow('frame',300,300)
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter(r"C:\Users\Phili\OneDrive - Danmarks Tekniske Universitet\Bachelorprojekt\Videoer\Algae_Vid_6croppedBW.mp4",fourcc, fps,(x2 - x1, y2 - y1),False)

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    fgmask = fgbg.apply(frame)
    #fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

    cv.imshow('Frame', frame)
    cv.imshow('FG MASK Frame', fgmask)
    out.write(fgmask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break


out.release()
cap.release()
cv.destroyAllWindows()