#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 12:03:29 2023

@author: joakimpihl
"""

#Load necessary packages
import cv2
import numpy as np
import pandas as pd

#%%
#Load timestamps
timestamps = pd.read_csv('/Users/joakimpihl/Desktop/Algae experiment 5/Time Stamps - sweep.csv', delimiter=';')
timestamps = timestamps['Frequency sweep'].tolist()
timestamps = np.array(timestamps[1:len(timestamps)])

#%%
#Find time indeces

indeces = np.array([0])
n = 0

for (i,j) in enumerate(timestamps):
    if j == 0 and i > 0:
        n += 1
    if (n == 10) and (j != 0):
        indeces = np.append(indeces, i-n)
        indeces = np.append(indeces, i+1)
        n = 0
        

