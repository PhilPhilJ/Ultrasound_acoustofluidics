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

df = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6/Resonance freq.csv', delimiter=',', encoding='utf-8')
freq = np.array(df['Frequency (MHz)'].tolist())
focus_time = np.array(df['Focusing time (99.99%)'].tolist())
#Unusually quick focussing time at 1.84MHz
#focus_time = np.delete(focus_time, 0)
#freq = np.delete(freq, 0)

#Remove negative values from data
focus_time_new = np.empty(0)
freq_new = np.empty(0)

for i,j in enumerate(focus_time):
    if j>0:
        focus_time_new = np.append(focus_time_new, j)
        freq_new = np.append(freq_new, freq[i])

#Fitting to lorentzian peak
def func(x, x0, w, h):
    return (h*w**2)/(w**2+(x-x0)**2)

popt, pcov = curve_fit(func, freq_new, 1/focus_time_new, bounds=([1.88, 0, 0], [1.91, 0.05, 0.5]))

#Generate data from fit
xdata = np.linspace(1.85, 1.95, 1000)

ydata = func(xdata, *popt) ## Curvefit doesn't work - too few data points??

#Plotting 1/t vs. freq
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(freq_new, 1/focus_time_new, 'ro', markersize='10')
ax.plot(xdata, ydata, 'r--')

ax.set_xlabel(r'Frequency [MHz]', fontsize='17.5')
ax.set_ylabel(r'1/Time [$\mathrm{s}^{-1}$]', fontsize='17.5')

plt.savefig('path', dpi=300, bbox_inches='tight')
#Generate csv file with filtered data
df_write = pd.DataFrame({'Frequency (MHz)':freq_new, 'Focusing time (99.99%)':focus_time_new})
df_write.to_csv('path', sep=',')