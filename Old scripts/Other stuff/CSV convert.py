#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 22:03:05 2023

@author: joakimpihl
"""

import pandas as pd
import numpy as np
import csv

data = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/CSV to bruus/New_Exp_1.89.csv', delimiter=';', encoding='utf-8')

time = np.array(data['Time'].tolist())
ydata = np.array(data['Relative intensity'].tolist())

time = np.round(time, 4)
ydata = np.round(ydata, 7)

df = pd.DataFrame({'Time':time, 'Relative intensity':ydata})
df.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/CSV to bruus/1.89.csv', sep=',', encoding='utf-8')