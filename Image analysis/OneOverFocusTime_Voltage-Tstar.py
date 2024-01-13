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
t_star = t_star[24:len(voltage)]
voltage = voltage[24:len(voltage)]



reciprocal_t_star = 1/t_star
voltage_squared = voltage**2

#%%
#Fitting straight line - log(y) = log(b') * log(x') + log(a')
def func(x,a, b):
    return a*x + b

popt, pcov = curve_fit(func, voltage, reciprocal_t_star)

#Generate data from fit
xdata = np.linspace(0, max(voltage)*1.1, 3000)

ydata = func(xdata, *popt) 

residuals = reciprocal_t_star - func(voltage_squared, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((reciprocal_t_star-np.mean(reciprocal_t_star))**2)
r_squared = 1 - (ss_res / ss_tot)

#%%
plt.close('all')
#Plotting 1/t vs. freq

fig, ax = plt.subplots(figsize=(10,10))
ax.plot(voltage, reciprocal_t_star,'ro', markersize='10', label='Data')
ax.plot(xdata, ydata, linestyle='dashdot', color ='black', label=f'Fit (a = {round(popt[0], 3)}, b = {round(popt[1],3)})')

ax.set_xlabel(r'Voltage, $U$ (V)', fontsize='17.5')
ax.set_ylabel(r'1/$t^*$ ($\mathrm{s}^{-1}$)', fontsize='17.5')
plt.legend(loc='upper left')
#%%
plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Voltage sweep 1/VoltageTstarCorrelation_using_power_2.png', dpi=300, bbox_inches='tight')


