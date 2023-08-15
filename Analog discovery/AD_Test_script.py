#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 17:53:34 2023

@author: joakimpihl
"""

#import serial, time
import cv2
import sys
#sys.path.append('C:/Program Files (x86)/Digilent/WaveFormsSDK/samples/py')
sys.path.append('/Applications/WaveForms.app/Contents/Resources/SDK/samples/py')
sys.path.append('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Repo/Algae-Ultrasound-Bachelor project/Analog discovery')
from AD_funcGen import *

print('Press ESC to close the window')

i = 1

while i>0:
    k = cv2.waitKey(0)
    img = cv2.imread('/Users/joakimpihl/Desktop/img1.jpeg') #Load an img to be displayed (Simulate video feed)
    cv2.imshow('Picture', img)
    
    if k == 27: # press ESC
        cv2.destroyWindow('Picture') #Closes all windows
        break
    if k == 102: # press f
        funcGen()
    if k == 70: # press F
        Connect()
        funcGen(freq=3.82)
        
    if k == 103: # press g
        funcStop()