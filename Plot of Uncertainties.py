#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:02:59 2024

@author: joakimpihl
"""

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis - 2/Uncertainties.csv', delimiter=',', encoding='utf-8')
freq = np.array(df['Frequency'].tolist())
rel_uncer = np.array(df['t_star uncertainty (relative: %)'].tolist())


mean_uncer = np.mean(rel_uncer)
sd_uncer = np.std(rel_uncer)


plt.close('all')
fig, ax = plt.subplots(figsize=(10,7.5))
plt.rcParams.update({'font.size': 12})
ax.plot(freq, rel_uncer, 'ro', label='Uncertainty data', markersize='7.5')
ax.hlines(y=mean_uncer, xmin=0, xmax=2, color='black', linestyle='dashdot', label='Mean')
ax.hlines(y=mean_uncer+sd_uncer, xmin=0, xmax=2, color='silver', linestyle='dashdot')
ax.hlines(y=mean_uncer-sd_uncer, xmin=0, xmax=2, color='silver', linestyle='dashdot')


ax.set_xlim(left=min(freq)-0.005, right=max(freq)+0.005)
ax.set_xlabel(r'Frequency [MHz]', fontsize='17.5')
ax.set_ylabel(r'Relative uncertainty', fontsize='17.5')

plt.savefig('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Results/ErrorAnalysis - 2/UncertaintyPlot.png', dpi=300, bbox_inches='tight')