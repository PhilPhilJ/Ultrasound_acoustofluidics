#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 14:48:27 2023

@author: joakimpihl
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import sys, os
sys.path.append('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Ultrasound_acoustofluidics/')
from Moving_Average import *

#%%
#Load data
df_1 = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/1.91MHz/Resonance freq.csv', delimiter=',', encoding='utf-8')
freq = df_1['Frequency (MHz)'].iloc[1].tolist()
t_stars = np.array(df_1['t_star'].tolist())

t_stars_mean = np.mean(t_stars[t_stars<60])
t_stars_sd = np.std(t_stars[t_stars<60])
delta_t_star = t_stars_mean**(-2) * t_stars_sd

df_write = pd.DataFrame({'Frequency':[freq], 't_star':[t_stars_mean], 't_star uncertainty':[t_stars_sd], 't_star uncertainty (relative: %)':[t_stars_sd/t_stars_mean], 'Reciprocal t_star':[1/t_stars_mean], 'Reciprocal t_star uncertainty':[delta_t_star], 'Reciprocal t_star uncertainty (relative: %)':[delta_t_star/(1/t_stars_mean)]})

#%%

if os.path.exists('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/Uncertainties.csv') != True:
    df_write.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/Uncertainties.csv', sep=',')
else:
    df_write.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/Uncertainties.csv', sep=',', header=False, mode='a')

