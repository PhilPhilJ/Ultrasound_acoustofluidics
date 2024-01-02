#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:20:14 2024

@author: joakimpihl
"""

#Load necessary packages
import cv2, os, sys
sys.path.append('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Ultrasound_acoustofluidics/')
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

#%%

#vid_num = 8
for vid_num in range(1,21):
    path = '/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/1.886MHz/I_norm/I_norm run'+str(vid_num)+'.csv'
    path_out = '/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/1.886MHz/'
    
    timestamps = np.array(pd.read_csv(path, sep=',', encoding='utf-8')['Timestamps'].tolist())
    intensities = np.array(pd.read_csv(path, sep=',', encoding='utf-8')['Normalized intensity'].tolist())
    
    alpha = 0.2
    k = np.pi*(1-alpha)/2 
    
    def func(t, t_star, R, z): #Define function which data is fitted to
        return 1-R/k*np.arctan(np.tan(k)*np.exp(-t/t_star)+z)
        
    popt, pcov = curve_fit(func, timestamps, meaned_I) #Fitting 
    
    t_star = popt[0]
    R_fit = popt[1]
    
    #Generate fitting data to overlay experimental data
    xdata_time = np.linspace(timestamps[0], timestamps[-1], 4000)
    ydata = func(xdata_time, *popt)
    
    t_star_e = format(t_star, ".1e")
    R_fit_e = format(R_fit, ".1e")
    
    residuals = meaned_I - func(timestamps, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((meaned_I-np.mean(meaned_I))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # /Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis/1.886MHz/Resonance freq_v2.csv
    fig, ax = plt.subplots(figsize=(10,7.5))
    ax.hlines(y=1-R_fit/(1-alpha), xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
    ax.hlines(y=1, xmin=timestamps[0], xmax=timestamps[-1], color='silver', alpha=1, linestyle='dashdot', label='_nolegend_')
    ax.scatter(timestamps, meaned_I, marker='o', color='red', label='Data')
    ax.plot(xdata_time, ydata, linestyle='dashdot', color='black', label=f'Fit ($t^*$ = {t_star_e}, R = {R_fit_e})')
    
    #plt.ylim((0.9955, 1.0008))
    
    plt.title('Run '+str(vid_num)+' and' +r' MHz (Fitting parameters: $t^*$ and R)', fontsize='20')
        
    ax.set_xlabel(r'Time ($\mathrm{s}$)', fontsize='17.5')
    ax.set_ylabel(r'$\mathrm{I/I_{max}}$', fontsize='17.5')
    
    plt.legend(loc='lower right')
    
    plt.savefig(path_out + 'Plots_ave/run '+str(vid_num)+' MHz.png', dpi=300, bbox_inches='tight')
        
    df = pd.DataFrame({'Run':[vid_num], 't_star':[t_star], 'alpha':[alpha], 'R (Fit)':[R_fit], 'R squared':[r_squared]})
    
    if os.path.exists(path_out + 'Resonance freq_ave.csv') != True:
        df.to_csv(path_out + 'Resonance freq_ave.csv', sep=',')
    else:
        df.to_csv(path_out + 'Resonance freq_ave.csv', sep=',', header=False, mode='a')

