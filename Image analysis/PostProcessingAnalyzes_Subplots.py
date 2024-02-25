#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 18:58:20 2024

@author: joakimpihl
"""

#Load necessary packages
import cv2, os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

#%%

#vid_num = 8

plt.close('all')
path_1 = '/Users/joakimpihl/Desktop/V_sweep_LC/I_norm/I_norm run 1.csv'
path_2 = '/Users/joakimpihl/Desktop/V_sweep_LC/I_norm/I_norm run 2.csv'
path_out = '/Users/joakimpihl/Desktop/V_sweep_LC/'

timestamps_1 = np.array(pd.read_csv(path_1, sep=',', encoding='utf-8')['Timestamps'].tolist())
intensities_1 = np.array(pd.read_csv(path_1, sep=',', encoding='utf-8')['Normalized intensity'].tolist())

timestamps_2 = np.array(pd.read_csv(path_2, sep=',', encoding='utf-8')['Timestamps'].tolist())
intensities_2 = np.array(pd.read_csv(path_2, sep=',', encoding='utf-8')['Normalized intensity'].tolist())

t_index_0_1 = np.argmin(np.abs(timestamps_1))

t_index_0_2 = np.argmin(np.abs(timestamps_2))


alpha = 0.2
k = np.pi*(1-alpha)/2 

def func(t, t_star, R, z): #Define function which data is fitted to
    return 1-R/k*np.arctan(np.tan(k)*np.exp(-t/t_star)+z)
    
popt_1, pcov_1 = curve_fit(func, timestamps_1[t_index_0_1:], intensities_1[t_index_0_1:]) #Fitting 
popt_2, pcov_2 = curve_fit(func, timestamps_2[t_index_0_2:], intensities_2[t_index_0_2:]) #Fitting

R_fit_1 = popt_1[1]
R_fit_2 = popt_2[1] 

#Generate fitting data to overlay experimental data
xdata_time_1 = np.linspace(timestamps_1[0], timestamps_1[-1], 4000)
xdata_time_2 = np.linspace(timestamps_2[0], timestamps_2[-1], 4000)
ydata_1 = func(xdata_time_1, *popt_1)
ydata_2 = func(xdata_time_2, *popt_2)


# =============================================================================
# residuals = intensities - func(timestamps, *popt)
# ss_res = np.sum(residuals**2)
# ss_tot = np.sum((intensities-np.mean(intensities))**2)
# r_squared = 1 - (ss_res / ss_tot)
# =============================================================================

# /Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/1.886MHz/Resonance freq_v2.csv
fig, ax = plt.subplots(1,2, figsize=(12.5,6.25))
ax[0].hlines(y=1-R_fit_1/(1-alpha), xmin=timestamps_1[0], xmax=timestamps_1[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax[0].hlines(y=1, xmin=timestamps_1[0], xmax=timestamps_1[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax[0].scatter(timestamps_1, intensities_1, marker='o', color='red', label='Data')
ax[0].plot(xdata_time_1, ydata_1, linestyle='dashdot', color='black', label=f'Fit')

ax[1].hlines(y=1-R_fit_2/(1-alpha), xmin=timestamps_2[0], xmax=timestamps_2[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax[1].hlines(y=1, xmin=timestamps_2[0], xmax=timestamps_2[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax[1].scatter(timestamps_2, intensities_2, marker='o', color='red', label='Data')
ax[1].plot(xdata_time_2, ydata_2, linestyle='dashdot', color='black', label=f'Fit')

#plt.ylim((0.9955, 1.0008))

#plt.title('Run '+str(vid_num)+' and' +r' MHz (Fitting parameters: $t^*$ and R)', fontsize='20')
plt.rcParams.update({'font.size': 15})
ax[0].set_xlabel(r'(a) Time [$\mathrm{s}$]', fontsize='20')
ax[1].set_xlabel(r'(b) Time [$\mathrm{s}$]', fontsize='20')
ax[0].set_ylabel(r'$\mathrm{I/I_{max}}$', fontsize='20')

ax[0].legend(loc='lower right')
ax[1].legend(loc='lower right')


#%%
plt.savefig(path_out + 'subplots.png', dpi=300, bbox_inches='tight')
    
#df = pd.DataFrame({'Run':[vid_num], 't_star':[t_star], 'alpha':[alpha], 'R (Fit)':[R_fit], 'R squared':[r_squared]})
