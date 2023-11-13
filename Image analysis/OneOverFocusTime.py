#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 21:41:48 2023

@author: joakimpihl
"""

#Load necessary packages
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

df = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Resonance freq - Exp 2/Resonance freq - Exp 2.csv', delimiter=';', encoding='utf-8')
freq = np.array(df['Frequency (MHz)'].tolist())
focus_time = np.array(df['Focusing time (99.99%)'].tolist())

#%%
def func(x, x0, w, h):
    return (h*w**2)/(w**2+(x-x0)**2)

popt, pcov = curve_fit(func, freq, (1/focus_time), bounds=(0.1, [1.9, 10, 0.5]))
# =============================================================================
# popt_high, pcov_high = curve_fit(func, freq[0:9], (1/focus_time[0:9]), bounds=(0.1, [1.9, 10, 0.5]))
# popt_low, pcov_low = curve_fit(func, freq[10:-1], (1/focus_time[10:-1]))
# =============================================================================

xdata = np.linspace(1.85, 1.93, 1000)

ydata = func(xdata, *popt) ## Curvefit doesn't work - too few data points??
# =============================================================================
# ydata_high = func(xdata, *popt_high) ## Curvefit doesn't work - too few data points??
# ydata_low = func(xdata, *popt_low)
# =============================================================================
# =============================================================================
# ydata_high = func(xdata, 1.885, 0.03, 0.16)
# ydata_low = func(xdata, 1.896, 0.03, 0.065)
# 
# =============================================================================
#%%
#Plotting 1/t vs. freq

fig, ax = plt.subplots(figsize=(10,10))
ax.plot(freq, 1/focus_time, 'ro', markersize='10')
ax.plot(xdata, ydata, 'r--')
# =============================================================================
# ax.plot(freq[0:9], 1/focus_time[0:9], 'ro', markersize='10')
# ax.plot(freq[10:-1], 1/focus_time[10:-1], 'b+', markersize='12')
# ax.plot(xdata, ydata_high, 'r--')
# ax.plot(xdata, ydata_low, 'b--')
# =============================================================================
ax.set_xlabel(r'Frequency [MHz]', fontsize='17.5')
ax.set_ylabel(r'1/Time [$\mathrm{s}^{-1}$]', fontsize='17.5')
