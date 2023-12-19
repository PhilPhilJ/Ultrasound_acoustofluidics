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

df = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/Resonance freq_v2.csv', delimiter=',', encoding='utf-8')
freq = np.array(df['Frequency (MHz)'].tolist())
t_star = np.array(df['t_star'].tolist())
reciprocal_t_star = 1/t_star
error = np.array(df['St dev on t_star'].tolist())
#Unusually quick focussing time at 1.84MHz
#focus_time = np.delete(focus_time, 0)
#freq = np.delete(freq, 0)
#%%
#Remove negative values from data
# focus_time_new = np.empty(0)
# freq_new = np.empty(0)

# for i,j in enumerate(focus_time):
#     if j>0:
#         focus_time_new = np.append(focus_time_new, j)
#         freq_new = np.append(freq_new, freq[i])
#%%
#Fitting to lorentzian peak
def func(x, x1, w1, h1): #x2, w2, h2):
    return (h1*w1**2)/(w1**2+(x-x1)**2)# + (h2*w2**2)/(w2**2+(x-x2)**2)

#popt, pcov = curve_fit(func, freq_new, 1/focus_time_new, bounds=([1.88, 0, 0], [1.91, 0.05, 0.5]))
popt, pcov = curve_fit(func, freq, reciprocal_t_star, bounds=([1.895, 0, 0], [1.90, 0.05, 2])) #bounds=([1.887, 0, 0, 1.895, 0, 0], [1.89, 0.05, 2, 1.90, 0.05, 2]


#Generate data from fit
xdata = np.linspace(min(freq)-0.001, max(freq)+0.001, 1000)

ydata = func(xdata, *popt) 

residuals = reciprocal_t_star - func(freq, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((reciprocal_t_star-np.mean(reciprocal_t_star))**2)
r_squared = round(1 - (ss_res / ss_tot), 2)
r_squared_2 = 1 - (ss_res / ss_tot)

#%%
#Plotting 1/t vs. freq
max_freq=round(float(freq[reciprocal_t_star==max(reciprocal_t_star)]),4)
min_freq=round(float(freq[11]),4)
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(freq, reciprocal_t_star,'ro', markersize='10', label='Corrected data')
ax.plot(freq[reciprocal_t_star==max(reciprocal_t_star)], reciprocal_t_star[reciprocal_t_star==max(reciprocal_t_star)],'o', markersize='10', label=f'Min focussing time (f = {max_freq} MHz)')
ax.plot(freq[11], reciprocal_t_star[11], color= 'tab:green', marker='o', markersize='10', label=f'Max focussing time (f = {min_freq} MHz)')
ax.plot(xdata, ydata, linestyle='dashdot', color ='black', label=f'Fit ($r^2$={r_squared})')

ax.set_xlabel(r'Frequency [MHz]', fontsize='17.5')
ax.set_ylabel(r'1/$t^*$ [$\mathrm{s}^{-1}$]', fontsize='17.5')
plt.legend()
plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/Resonance.png', dpi=300, bbox_inches='tight')
#Generate csv file with filtered data
#df_write = pd.DataFrame({'Frequency (MHz)':freq_new, 'Focusing time (99.99%)':focus_time_new})
#df_write.to_csv('path', sep=',')