#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:18:57 2024

@author: joakimpihl
"""

#Load necessary packages
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

voltage_LC = np.array(pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Voltage sweep 1/Resonance freq.csv', delimiter=',', encoding='utf-8')['Voltage (V)'].tolist())
t_star_LC = np.array(pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Voltage sweep 1/Resonance freq.csv', delimiter=',', encoding='utf-8')['t_star'].tolist())
voltage_HC = np.array(pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/HC_Voltage sweep/Resonance freq.csv', delimiter=',', encoding='utf-8')['Voltage'].tolist())
t_star_HC = np.array(pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/HC_Voltage sweep/Resonance freq_diff_fit.csv', delimiter=',', encoding='utf-8')['t_star'].tolist())
voltage_LC = voltage_LC*(20**0.5)
voltage_HC = voltage_HC*(10**0.5)

reciprocal_t_star_LC = 1/t_star_LC
reciprocal_t_star_HC = 1/t_star_HC


#%%
#Fitting straight line - log(y) = log(b') * log(x') + log(a')
def func(x,a,b):
    return a * x + b

popt_LC, pcov_HC = curve_fit(func, voltage_LC**2, reciprocal_t_star_LC)
popt_HC, pcov_HC = curve_fit(func, voltage_HC[24:]**2, reciprocal_t_star_HC[24:])

#Generate data from fit
xdata_LC = np.linspace(0, (2.1*(20**0.5))**2, 3000)
xdata_HC = np.linspace(0, (2.1*(10**0.5))**2, 3000)

ydata_LC = func(xdata_LC, *popt_LC) 
ydata_HC = func(xdata_HC, *popt_HC) 

yerror_LC = abs(reciprocal_t_star_LC)*0.06
yerror_HC = abs(reciprocal_t_star_HC[24:])*0.06

# =============================================================================
# residuals = reciprocal_t_star[24:]- func(voltage[24:]**2, *popt)
# ss_res = np.sum(residuals**2)
# ss_tot = np.sum((reciprocal_t_star[24:]-np.mean(reciprocal_t_star[24:]))**2)
# r_squared = 1 - (ss_res / ss_tot)
# =============================================================================

#%%
plt.close('all')
#Plotting 1/t vs. freq

fig, ax = plt.subplots(1,2, figsize=(15,7))
plt.rcParams.update({'font.size': 15})
ax[0].errorbar(voltage_LC**2, reciprocal_t_star_LC, yerr=yerror_LC, errorevery=1, fmt='ro', markersize='10', label='Data')
ax[0].plot(xdata_LC, ydata_LC, linestyle='dashdot', color ='black', label=f'Fit')
ax[0].set_xlabel(r'$U_{pp}^2$ [$V^2$]', fontsize='20')
ax[0].hlines(y=(popt_LC[0]*50+popt_LC[1]), xmin=50, xmax=70, linestyle='dotted', color='black')
ax[0].vlines(x=70, ymin=(popt_LC[0]*50+popt_LC[1]), ymax=(popt_LC[0]*70+popt_LC[1]), linestyle='dotted', color='black')
#ax[0].set_ylabel(r'$\log_{10}(1/t^*)$ [$\log_{10}(\mathrm{s}^{-1}$]', fontsize='20')
ax[0].legend(loc='lower right')

ax[1].plot(xdata_HC, ydata_HC, linestyle='dashdot', color ='black', label=f'Fit')
ax[1].errorbar(voltage_HC[24:]**2, reciprocal_t_star_HC[24:], yerr=yerror_HC, errorevery=1, fmt='ro', markersize='10', label='Data')
ax[1].plot(voltage_HC[:24]**2, reciprocal_t_star_HC[:24],'ro', markersize='10', fillstyle='none', label='Excluded data')
ax[1].hlines(y=(popt_HC[0]*15+popt_HC[1]), xmin=15, xmax=35, linestyle='dotted', color='black')
ax[1].vlines(x=35, ymin=(popt_HC[0]*15+popt_HC[1]), ymax=(popt_HC[0]*35+popt_HC[1]), linestyle='dotted', color='black')
ax[1].set_xlabel(r'$U_{pp}^2$ [$V^2$]', fontsize='20')
#ax[1].set_ylabel(r'$\log_{10}(1/t^*)$ [$\log_{10}(\mathrm{s}^{-1}$]', fontsize='20')
ax[1].legend(loc='lower right')

# Add shared x label
#fig.text(0.5, 0.03, r'$\log_{10}(U_{pp})$ [$\log_{10}(U_{pp})$]', ha='center', va='center', fontsize=20)
# Add shared y label
fig.text(0.085, 0.5, r'$1/t^*$ [$\mathrm{s}^{-1}$]', ha='center', va='center', rotation='vertical', fontsize=20)

#%%
plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Images/U^2/VoltageTstarCorrelation2_withGain.png', dpi=300, bbox_inches='tight')


