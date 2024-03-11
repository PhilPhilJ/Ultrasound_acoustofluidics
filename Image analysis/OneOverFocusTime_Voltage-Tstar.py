#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:29:28 2024

@author: joakimpihl
"""

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

df = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/HC_Voltage sweep/Resonance freq_diff_fit.csv', delimiter=',', encoding='utf-8')
voltage = np.array(pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/HC_Voltage sweep/Resonance freq.csv', delimiter=',', encoding='utf-8')['Voltage'].tolist())
t_star = np.array(df['t_star'].tolist())



reciprocal_t_star = 1/t_star
voltage_squared = voltage**2


#%%
#Fitting straight line - log(y) = log(b') * log(x') + log(a')
def func(x,a,b):
    return a * x + b

popt, pcov = curve_fit(func, voltage[24:]**2, reciprocal_t_star[24:])

#Generate data from fit
xdata = np.linspace(min(voltage[24:]**2)-1, max(voltage[24:]**2)*1.1, 3000)

ydata = func(xdata, *popt) 
yerror = reciprocal_t_star[24:]*0.06

residuals = reciprocal_t_star[24:]- func(voltage[24:]**2, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((reciprocal_t_star[24:]-np.mean(reciprocal_t_star[24:]))**2)
r_squared = 1 - (ss_res / ss_tot)

#%%
plt.close('all')
#Plotting 1/t vs. freq

fig, ax = plt.subplots(figsize=(10,7.5))
ax.errorbar(voltage[24:]**2, reciprocal_t_star[24:], yerr=yerror, errorevery=5, fmt='ro', markersize='10', label='Data')
ax.plot(voltage[0:24]**2, reciprocal_t_star[0:24], 'ro', markersize='10', fillstyle='none', label='Excluded data')
ax.plot(xdata, ydata, linestyle='dashdot', color ='black', label=f'Fit')
plt.rcParams.update({'font.size': 15})
ax.set_xlabel(r'${U_{pp}}^2$ (V)', fontsize='20')
ax.set_ylabel(r'$1/t^*$ [$\mathrm{s}^{-1}$]', fontsize='20')
plt.legend(loc='upper left')
#%%
plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Images/U^2/VoltageTstarCorrelation_known_power_HC_w_excluded_data.png', dpi=300, bbox_inches='tight')


