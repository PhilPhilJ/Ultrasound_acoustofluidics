#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 20:53:55 2023

@author: joakimpihl
"""

#Load necessary packages
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os

plt.close('all')
# Video number
vid_num = 2
# Load data
timestamps = np.array(pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/Corrected I_norm/corrected I_norm run'+str(vid_num)+'.csv', delimiter=',', encoding='utf-8')['Timestamps'].tolist())
intensities = np.array(pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/Corrected I_norm/corrected I_norm run'+str(vid_num)+'.csv', delimiter=',', encoding='utf-8')['Normalized intensity'].tolist())

# Curve fitting
alpha = 0.20
k = np.pi*(1-alpha)/2
#%%
def func(t, t_star, R): #Define function which data is fitted to
    return 1-R/k*np.arctan(np.tan(k)*np.exp(-t/t_star))

popt, pcov = curve_fit(func, timestamps, intensities, bounds=([0.1, 0.0001],[40,0.01])) 

t_star = popt[0]
R_fit = popt[1]
t_star_e = format(t_star, ".1e")
R_fit_e = format(R_fit, ".1e")

#Generate data to plot
xdata =  np.linspace(timestamps[0],timestamps[-1], 5000)
ydata = func(xdata, t_star, R_fit)

#Compute r^2
residuals = intensities - func(timestamps, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((intensities-np.mean(intensities))**2)
r_squared = 1 - (ss_res / ss_tot)

#%%
plt.close('all')
#Plotting of data and fit
fig, ax = plt.subplots(figsize=(10,7.5))
ax.hlines(y=1-R_fit/(1-alpha), xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax.hlines(y=1, xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
ax.scatter(timestamps, intensities, marker='o', color='red', label='Data')
ax.plot(xdata, ydata, linestyle='dashdot', color='black', label=f'Fit ($t^*$ = {t_star_e}, R = {R_fit_e})')

plt.ylim((0.9945, 1.0008))

plt.title('Run '+str(vid_num)+ ' (Fitting parameters: $t^*$ and R)', fontsize='20')
    
ax.set_xlabel(r'Time ($\mathrm{s}$)', fontsize='17.5')
ax.set_ylabel(r'$\mathrm{I/I_{max}}$', fontsize='17.5')

plt.legend(loc='lower right')

print(r_squared)


#%%
plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/Corrected fits/run '+str(vid_num)+'.png', dpi=300, bbox_inches='tight')

df = pd.DataFrame({'Run':[vid_num], 't_star':[t_star], 'R squared':[r_squared]})

if os.path.exists('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/Corrected fits/Resonance freq (Corrected).csv') != True:
    df.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/Corrected fits/Resonance freq (Corrected).csv', sep=',')
else:
    df.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Focus sweep 6.3/Corrected fits/Resonance freq (Corrected).csv', sep=',', header=False, mode='a')
plt.close('all')