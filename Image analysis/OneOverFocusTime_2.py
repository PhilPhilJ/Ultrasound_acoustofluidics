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

df = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/Biiiig sweep/Resonance freq_diff_fit.csv', delimiter=',', encoding='utf-8')
freq = np.array(df['Frequency (MHz)'].tolist())
t_star = np.array(df['t_star'].tolist())

reciprocal_t_star = 1/t_star

#%%
#Fitting to lorentzian peak: fc = center frequency, Df = peak width, Lc = peak amplitude
def func(x, fc, Df, Lc, fc2, Df2, Lc2):
    return Lc/(1+((x-fc)/Df)**2) + Lc2/(1+((x-fc2)/Df2)**2)

def func2(x, fc, Df, Lc):
    return Lc/(1+((x-fc)/Df)**2)


#popt, pcov = curve_fit(func, freq_new, 1/focus_time_new, bounds=([1.88, 0, 0], [1.91, 0.05, 0.5]))
fit_freq = freq #np.concatenate((freq[11:22], freq[27:31]))
fit_reciprocal_t_star = reciprocal_t_star #np.concatenate((reciprocal_t_star[11:22], reciprocal_t_star[27:31]))
popt, pcov = curve_fit(func, fit_freq, fit_reciprocal_t_star, bounds=([1.894, 0, 0, 1.895, 0, 0], [1.9, 0.05, 2, 1.95, 0.05, 2]))


#Generate data from fit
xdata = np.linspace(min(freq)-0.001, max(freq)+0.001, 1000)

ydata = func(xdata, *popt) 

# Iterative solution
ydata_upper = ydata*1.06
ydata_lower = ydata*0.94


# Calculate residuals
residuals = reciprocal_t_star - func(fit_freq, *popt)

# Define threshold percentage (e.g., 10%)
threshold_percentage = 6

# Filter the array based on the threshold
filtered_indices = np.abs(residuals) / reciprocal_t_star * 100 < threshold_percentage
filtered_freq = freq[filtered_indices]
filtered_t_star = reciprocal_t_star[filtered_indices]

residuals = reciprocal_t_star - func(freq, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((reciprocal_t_star-np.mean(reciprocal_t_star))**2)
r_squared = round(1 - (ss_res / ss_tot), 2)
r_squared_2 = 1 - (ss_res / ss_tot)

#%%
plt.close('all')
#Plotting 1/t vs. freq
max_data=round(float(freq[reciprocal_t_star==max(reciprocal_t_star)]),6)
max_fit=round(float(xdata[ydata==max(ydata)]),6)

freq_near_fwhm = xdata[np.isclose(ydata, max(ydata)/2, atol=0.0075, rtol=0)]
if len(freq_near_fwhm) % 2 == 0:
    f_lower = np.mean(freq_near_fwhm[0:int(len(freq_near_fwhm)/2+1)])
    f_upper = np.mean(freq_near_fwhm[int(len(freq_near_fwhm)/2+1):len(freq_near_fwhm)])
elif len(freq_near_fwhm) % 2 != 0:
    raise(ValueError)
FWHM_fit = f_upper-f_lower
gain = max_fit/FWHM_fit

freq_near_fwhm = xdata[np.isclose(ydata, max(ydata)/2, atol=0.0075, rtol=0)]
if len(freq_near_fwhm) % 2 == 0:
    f_lower = np.mean(freq_near_fwhm[0:int(len(freq_near_fwhm)/2+1)])
    f_upper = np.mean(freq_near_fwhm[int(len(freq_near_fwhm)/2+1):len(freq_near_fwhm)])
elif len(freq_near_fwhm) % 2 != 0:
    raise(ValueError)
FWHM_fit = f_upper-f_lower
gain = max_fit/FWHM_fit

fig, ax = plt.subplots(figsize=(10,7.5))
plt.fill_between(xdata, ydata_lower, ydata_upper, color='grey', alpha=0.3, interpolate=True, label='_nolabel_')
ax.plot(filtered_freq, filtered_t_star,'ro', markersize='10', label='Data')
#ax.plot(freq[freq != fit_freq], reciprocal_t_star[freq != fit_freq],'ro', markersize='10', label='_nolabel_', fillstyle='none')
#ax.plot(freq[reciprocal_t_star==max(reciprocal_t_star)], reciprocal_t_star[reciprocal_t_star==max(reciprocal_t_star)],'o', markersize='10', label=f'Min focussing time (f = {max_freq} MHz)')
#ax.plot(freq[11], reciprocal_t_star[11], color= 'tab:green', marker='o', markersize='10', label=f'Max focussing time (f = {min_freq} MHz)')
ax.plot(xdata, ydata, linestyle='solid', color ='black', label='Fit')
#ax.plot(xdata, ydata_upper, linestyle='dashed', color ='black', label='Fit')
#ax.plot(xdata, ydata_lower, linestyle='dashed', color ='black', label='Fit')
plt.rcParams.update({'font.size': 15})
ax.set_xlabel(r'Frequency [MHz]', fontsize='20')
ax.set_ylabel(r'1/$t^*$ [$\mathrm{s}^{-1}$]', fontsize='20')
plt.legend(loc='upper left')
#%%
plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Images/Resonance peak/Exp 3/ExtraMultiPeak/Resonance.png', dpi=300, bbox_inches='tight')
#Generate csv file with filtered data
f = open("/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Images/Resonance peak/Exp 3/ExtraMultiPeak/Resonance.txt", "x")
f.write(f'Fit r^2 = {r_squared_2} |Resonance frequency data = {max_data} MHz | Resonance frequency fit = {max_fit} MHz | FWHM = {FWHM_fit} | Gain fit = {gain} | Only filled dots are used for fitting')
f.close()
#df_write = pd.DataFrame({'Frequency (MHz)':freq_new, 'Focusing time (99.99%)':focus_time_new})
#df_write.to_csv('path', sep=',')

