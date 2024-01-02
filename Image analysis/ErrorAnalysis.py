#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 14:48:27 2023

@author: joakimpihl
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from Moving_Average import *

#%%
#Load data
df_1 = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/1.886MHz/Resonance freq_v2.csv', delimiter=',', encoding='utf-8')
raw_t_stars = np.array([df_1['t_star'].tolist()])

raw_t_stars_mean = np.mean(raw_t_stars)
raw_t_stars_sd = np.std(raw_t_stars)

#%%


