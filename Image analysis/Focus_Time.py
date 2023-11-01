#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:18:24 2023

@author: joakimpihl
"""

#Load necessary packages
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import pandas as pd
from scipy.optimize import curve_fit
from scipy import stats

#%%
#Load video, background and timestamps for video
exp_num = 5 #Choose experiment number
vid_num = 5 #choose video number
###
# =============================================================================
# vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/Algae experiment '+str(exp_num)+'/'+str(vid_num)+'_run/focus_'+str(vid_num)+'.mp4') #Loads the video
# vid_back = cv2.VideoCapture('/Users/joakimpihl/Desktop/Algae experiment '+str(exp_num)+'/'+str(vid_num)+'_run/backgroung_'+str(vid_num)+'.mp4') #Loads the background video
# timestamps = pd.read_csv('/Users/joakimpihl/Desktop/Algae experiment '+str(exp_num)+'/Time Stamps - sweep.csv', delimiter=';')
# timestamps = timestamps['Frequency sweep'].tolist()
# timestamps = np.array(timestamps[1:len(timestamps)])
# =============================================================================
vid = cv2.VideoCapture('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/DoubleFreqTest 1.885/run'+str(vid_num)+'.mp4') #Loads the video
vid_back = cv2.VideoCapture('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/DoubleFreqTest 1.885/runbackground.mp4') #Loads the background video
timestamps = pd.read_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/DoubleFreqTest 1.885/Time Stamps'+str(vid_num)+'.csv', delimiter=';', encoding='utf-8')
timestamps = timestamps['Frame time'].tolist()
freq = timestamps[0]
timestamps = np.array(timestamps[1:len(timestamps)])
timestamps = timestamps-timestamps[0]
#%%
########################################## Find start and end indeces for each video ##########################################
# =============================================================================
# indeces = np.array([0])
# n = 0
# 
# for (i,j) in enumerate(timestamps):
#     if j == 0 and i > 0:
#         n += 1
#     if (n == 10) and (j != 0):
#         indeces = np.append(indeces, i-n)
#         indeces = np.append(indeces, i+1)
#         n = 0 
# =============================================================================
########################################## Find start and end indeces for each video ##########################################
#%%
# =============================================================================
# timestamps = timestamps[indeces[2*vid_num-2]:indeces[2*vid_num-1]]
# timestamps = timestamps-timestamps[0]
# =============================================================================
#%%
#Crop image data 
####################################### Define functions start #######################################
def update(val): # The function to be called anytime a slider's value changes
    global slider_val
    slider_val = val
    vert_line.set_xdata(val)
    fig.canvas.draw_idle()
    
def assign_min(event): #A function that assigns the threshold value given by the slider
    global index_left_side
    index_left_side = globals()['slider_val']
    print('The min threshold has been set to: ' + str(round(index_left_side,0)))
    if 'index_right_side' in globals():
        plt.close(fig)

def assign_max(event): #A function that assigns the threshold value given by the slider
    global index_right_side
    index_right_side = globals()['slider_val']
    print('The max threshold has been set to: ' + str(round(index_right_side,0)))
    if 'index_left_side' in globals():
        plt.close(fig)
####################################### Define functions end #######################################

#Reads the fist frame
ret, frame = vid_back.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
frame_length = np.size(frame, axis=0)

####################################### Plotting intensities overlayed image of channel #######################################
fig, ax1 = plt.subplots()
fig.set_size_inches(20/2.54, 15/2.54)

ax1.set_xlabel('x-direction [px]') #Image of channel
ax1.set_ylabel('y-dricetion [px]')
ax1.imshow(frame,cmap='gray')

ax2 = ax1.twinx() #Intensities
ax2.set_ylabel('Intensity [0;255]')
ax2.plot(np.arange(0, frame_length), np.mean(frame, axis=0), color='r')

#ax3 = ax1.twinx() #Intensities
ax3 = ax1.twinx()
ax3.axis('off')
vert_line = plt.axvline(x=frame_length/3, color = 'b')

# Make a horizontal slider to control the line position.
axpos = fig.add_axes([0.2, 0, 0.65, 0.03])
pos_slider = Slider(ax=axpos, label='Position', valmin=0, valmax=frame_length, valinit=frame_length/3)

# register the update function with each slider
pos_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to accept the slider value.
min_val = fig.add_axes([0.0125, 0.05, 0.1, 0.04])
max_val = fig.add_axes([0.875, 0.05, 0.1, 0.04])
button_min = Button(min_val, 'Min', hovercolor='0.975')
button_max = Button(max_val, 'Max', hovercolor='0.975')

button_min.on_clicked(assign_min)
button_max.on_clicked(assign_max)

#%%
#Define boundaries 
min_bound = int(round(index_left_side,0))
max_bound = int(round(index_right_side,0))
mm_per_px = 400/(max_bound-min_bound) # conversion factor: um/px

###################################### Generate background and intensity matrix ######################################
ret, frame = vid.read()#Reads the fist frame
n_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) #Frames in video
#CHANGE DEPENDING ON WHICH VIDEO IS USED
timestamps = timestamps[0:n_frames] 
##################################
n_frames_back = int(vid_back.get(cv2.CAP_PROP_FRAME_COUNT)) #Frames in background video
plt.close('all') #Close all plots for good measure
#Define empty arrays to contain data
intensities = np.empty(np.size(frame[:,min_bound:max_bound], axis=1))
background = np.empty(np.size(frame[:,min_bound:max_bound], axis=1))

#Generate background
for i in range(n_frames_back-1):
    ret_2, back_frame = vid_back.read()
    back_frame = cv2.cvtColor(back_frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    back_frame = back_frame[:,min_bound:max_bound]
    back_frame_mean = np.mean(back_frame, axis=0)
    background = np.vstack([background, back_frame_mean])
    
#Generate matrix containing vertically meaned intensities
for i in range(n_frames-1):
    ret, frame = vid.read() #Reads the fist frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
    frame = frame[:,min_bound:max_bound]
    frame_mean = np.mean(frame, axis=0)
    intensities = np.vstack([intensities, frame_mean])

background = background[1:np.size(background, axis=0),:]
mean_background = np.mean(background, axis=0)

intensities = intensities[1:np.size(intensities,axis=0),:]
timestamps = timestamps[1:len(timestamps)]

#Cleaning up memory
if 'vid' in globals():
    del frame, ret, ret_2, frame_mean, back_frame, back_frame_mean, vid, vid_back, slider_val, pos_slider, button_min, button_max
# =============================================================================
# ######################################### Wanna take a look at bakcground data? #########################################
# user_input = input('Do you wanna visualize the background data? [y/n]')
# 
# if user_input == 'y':
#     plt.close('all')
# 
#     fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
#     back_over_time = np.zeros(n_frames_back)
# 
#     def update(val):
#         frame_val = int(Slider_val.val)-1
#         plot_of_background.set_ydata(background[frame_val,:])
#         fig.canvas.draw_idle()
# 
#     fig.set_size_inches(30/2.54, 25/2.54)
#     fig.suptitle('Plot of background intensity, background intensity over time, and mean background intensity', fontsize='15') 
#     # Set common labels
#     fig.text(0.5, 0.025, 'X-position [px]', ha='center', va='center', fontsize='12.5')
#     fig.text(0.025, 0.5, 'Intensity [0:255]', ha='center', va='center', rotation='vertical', fontsize='12.5')
#     fig.tight_layout(pad=3)
# 
#     ax1.plot(np.arange(min_bound,max_bound), mean_background, color='black', linestyle='dashdot')
#     plot_of_background, = ax1.plot(np.arange(min_bound,max_bound), background[0,:], color='r')
#     ax_slider = plt.axes([0.125, 0.915, 0.80, 0.04], facecolor="red")
#     Slider_val = Slider(ax_slider, 'Frame', 1, np.size(background, axis=0), valinit=1, valstep=1)
#     Slider_val.on_changed(update)
#     ax1.set_title('Background intensity', fontsize='12.5')
#     ax1.set_ylim(np.mean(mean_background)*0.95, np.mean(mean_background)*1.05)
# 
# 
#     for i in range(n_frames_back-1):
#         ax2.plot(np.arange(min_bound,max_bound), background[i,:], color='r')
#         back_over_time[i] = np.mean(background[i,1430:1800])
#         
#     ax2.set_title('Background intensity over time', fontsize='12.5')
# 
#     ax3.plot(np.arange(min_bound,max_bound), mean_background, color='r')
#     ax3.set_title('Mean background', fontsize='12.5')
# 
# ######################################### Wanna take a look at intensity data? #########################################
# user_input = input('Do you wanna visualize the intensity data? [y/n]')
# 
# if user_input == 'y':
#     plt.close('all')
#     del plot_of_background
# 
#     fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, sharey=False)
#     
#     def update_2(val):
#         frame_val = int(Slider_val.val)-1
#         plot_of_intensities.set_ydata(intensities[frame_val,:])
#         plot_of_intensities_2.set_ydata(intensities[frame_val,:]-mean_background)
#         fig.canvas.draw_idle()
# 
#     fig.set_size_inches(30/2.54, 25/2.54)
#     fig.suptitle('Plot of Intensity, intensity over time, and mean intensity', fontsize='15') 
#     # Set common labels
#     fig.text(0.5, 0.025, 'X-position [px]', ha='center', va='center', fontsize='12.5')
#     fig.text(0.025, 0.5, 'Intensity [0:255]', ha='center', va='center', rotation='vertical', fontsize='12.5')
#     fig.tight_layout(pad=3)
# 
#     ax1.plot(np.arange(min_bound,max_bound), mean_background, color='black', linestyle='dashdot')
#     plot_of_intensities, = ax1.plot(np.arange(min_bound,max_bound), intensities[0,:], color='r')
#     ax_slider = plt.axes([0.125, 0.915, 0.80, 0.04], facecolor="red")
#     Slider_val = Slider(ax_slider, 'Frame', 1, np.size(intensities, axis=0), valinit=1, valstep=1)
#     Slider_val.on_changed(update_2)
#     ax1.set_title('Intensity', fontsize='12.5')
#     ax1.set_ylim([np.mean(mean_background)*0.875, np.mean(mean_background)*1.075])
# 
#     for i in range(np.size(intensities, axis=0)):
#         ax2.plot(np.arange(min_bound,max_bound), intensities[i,:], color='r')
#     ax2.set_title('Intensity over time', fontsize='12.5')
# 
#     ax3.plot(np.arange(min_bound,max_bound), mean_background-mean_background, color='black', linestyle='dashdot')
#     plot_of_intensities_2, = ax3.plot(np.arange(min_bound,max_bound), intensities[0,:]-mean_background, color='r')
#     Slider_val.on_changed(update_2)
#     ax3.set_title('Intensity with background subtracted', fontsize='12.5')
#     ax3.set_ylim([np.min(intensities-mean_background)-1, np.max(intensities-mean_background)+1])
# 
# 
#     for i in range(np.size(intensities, axis=0)):
#         ax4.plot(np.arange(min_bound,max_bound), intensities[i,:]-mean_background, color='r')
#     ax4.set_title('Intensity over time with background subtracted', fontsize='12.5')
# 
# ######################################### End look at intensity/background data? #########################################
# =============================================================================
#%%
intensities_sub_back = intensities - mean_background #Intensities subtracted background
I_rel = (-1)*intensities_sub_back/mean_background
######################################### 2/3D plot of intensities #########################################
plt.close('all')
fig, ax = plt.subplots(figsize=(10,10))
img = ax.imshow(np.flipud(np.rot90(I_rel)), cmap='plasma_r', extent=[timestamps[0], timestamps[-1], 0, 400], interpolation='nearest') 
######################################### Vertical lines where diff. videos start #########################################
# =============================================================================
# ax.vlines(x=int(timestamps[-1]/5), ymin=0, ymax=400)
# ax.vlines(x=int(timestamps[-1]*2/5), ymin=0, ymax=400)
# ax.vlines(x=int(timestamps[-1]*3/5), ymin=0, ymax=400)
# ax.vlines(x=int(timestamps[-1]*4/5), ymin=0, ymax=400)
# =============================================================================
ax.set_title('Some title', fontsize='25')
ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax.set_ylabel(r'Position [$\mathrm{\mu m}$]', fontsize='17.5')
ax.set_aspect(0.05)
plt.rcParams.update({'font.size': 10})
plt.colorbar(img, label='Relative drop in intensity', fraction=0.046, pad=0.04)

plt.show()

#%%
#3D plot
plt.close('all')
x = timestamps
y = np.linspace(0, (max_bound-min_bound)*mm_per_px, (max_bound-min_bound))
X, Y = np.meshgrid(x,y, indexing='xy')

plt.close('all')
fig = plt.figure(figsize=(10,10))

ax = plt.axes(projection='3d')
img3d = ax.plot_surface(X,Y,np.rot90(I_rel), cmap='plasma_r')
ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax.set_ylabel(r'Position [$\mathrm{\mu m}$]', fontsize='17.5')
ax.set_zlabel(r'Relative drop in intensity', fontsize='17.5')
ax.set_title('Some other title', fontsize='25')
fig.colorbar(img3d, label='Relative drop in intensity', fraction=0.046, pad=0.04, location='bottom')

#%%
#Define alpha region - The region which algae are focused into
alpha = 0.20
I_norm = np.empty([0])
delta = 0 #How much to skew/offcet alpha region

s1 = np.array([0, int(np.ceil((1/2*(1-alpha))*np.size(intensities, axis=1)))])
s2 = np.array([int(np.ceil((1/2*(1-alpha)+alpha)*np.size(intensities,axis=1))), -1])

#Define max intensity - Max value is defined to be the mean of the background video intensity
I_0 = np.sum(intensities[0,s1[0]:(s1[1]+delta)]) + np.sum(intensities[0,(s2[0]-delta):s2[1]])
I_max = np.sum(intensities[-1,s1[0]:(s1[1]+delta)]) + np.sum(intensities[-1,(s2[0]-delta):s2[1]])


#For each timestamp figure out the intensity the intensity relative to I_max
for (i,j) in enumerate(timestamps):
    if i < np.size(intensities,axis=0):
        i_1 = np.sum(intensities[i, 0:(s1[1]+delta)])
        i_2 = np.sum(intensities[i, int(np.ceil((1/2*(1-alpha)+alpha)*np.size(intensities,axis=1))):-1])
        
        I_t = np.sum([i_1, i_2])
        I_norm = np.append(I_norm, I_t/I_max)

R = 1-I_0/I_max
k = np.pi*(1-alpha)/2

#%%
plt.close('all')
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(timestamps, I_norm, 'o')
plt.ylim([0.999*min(I_norm),1.001*max(I_norm)])

ax.set_title('Some title', fontsize='25')
ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax.set_ylabel(r'$\frac{I}{I_{max}}$', fontsize='17.5')

I_norm_max = np.mean(I_norm[-5:-1])


ax.hlines(y=I_norm_max*0.9999, xmin=0, xmax=timestamps[-1])



######################################### Vertical lines where diff. videos start #########################################
# =============================================================================
# ax.vlines(x=int(timestamps[-1]/5), ymin=0.9*min(I_norm), ymax=1.1*max(I_norm))
# ax.vlines(x=int(timestamps[-1]*2/5), ymin=0.9*min(I_norm), ymax=1.1*max(I_norm))
# ax.vlines(x=int(timestamps[-1]*3/5), ymin=0.9*min(I_norm), ymax=1.1*max(I_norm))
# ax.vlines(x=int(timestamps[-1]*4/5), ymin=0.9*min(I_norm), ymax=1.1*max(I_norm))
# =============================================================================

#%%
fig2, ax2 = plt.subplots(figsize=(10,10))
img = ax2.imshow(np.flipud(np.rot90(I_rel)), cmap='plasma_r', extent=[timestamps[0], timestamps[-1], 0, 400], interpolation='nearest') 

######################################### Horizontal lines where diff. videos start #########################################
ax2.hlines(y=(s1[1]+delta)*mm_per_px, xmin=timestamps[0], xmax=timestamps[-1])
ax2.hlines(y=(s2[0]+delta)*mm_per_px, xmin=timestamps[0], xmax=timestamps[-1])
ax2.set_title('Some title', fontsize='25')
ax2.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax2.set_ylabel(r'Position [$\mathrm{\mu m}$]', fontsize='17.5')
ax2.set_aspect(0.05)
plt.rcParams.update({'font.size': 10})
plt.colorbar(img, label='Relative drop in intensity', fraction=0.046, pad=0.04)
#%%
def func(t, t_star):
    return 1-R/k*np.arctan(np.tan(k)*np.exp(-t/t_star))

popt, pcov = curve_fit(func, timestamps, I_norm)

t_star = popt[0]

xdata_time = np.linspace(0, timestamps[-1], 1000)
ydata = func(xdata_time, popt)


#%% 
#Find R^2
residuals = I_norm - func(timestamps, popt) #Find residual
ss_res = np.sum(residuals**2) #Find residual sum of squares

ss_tot = np.sum((I_norm-np.mean(I_norm))**2) #Total sum of squares

r_squared = 1 - (ss_res / ss_tot) #R squared of fit

#%%
#Find the prediction interval 100(1-a)% of the time time the PI will contain the ydata
a = 0.9998 #alpha level
n = len(I_norm) #number of observations
p = len(popt) #number of parameters
dof = n-2 #Degrees of freedom

t_ahalf = stats.t.ppf(a/2, dof) 
uL = np.empty(0)
lL = np.empty(0)

Sxx = np.sum((xdata_time-np.mean(xdata_time))**2)

for i,j in enumerate(xdata_time):
    uL = np.append(uL, ydata[i] + t_ahalf* np.sqrt(1 + 1/n + ((j-np.mean(xdata_time))**2)/Sxx))
    lL = np.append(lL, ydata[i] - t_ahalf* np.sqrt(1 + 1/n + ((j-np.mean(xdata_time))**2)/Sxx))  


#%%
plt.close('all')
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(np.linspace(0, timestamps[-1],1000), ydata, 'k--')
ax.plot(timestamps, I_norm, 'or')
ax.fill_between(xdata_time, lL, uL, color = 'black', alpha = 0.15)

ax.set_title('Normalized intensity vs. time (frequency [MHz]: '+str(freq)+')', fontsize='25')
ax.set_xlabel(r'Time [$\mathrm{s}$]', fontsize='17.5')
ax.set_ylabel(r'$\frac{I}{I_{max}}$', fontsize='17.5')

focus_time = 0

for i,j in enumerate(ydata):
    if focus_time == 0 and j >= 0.9999*max(ydata):
        focus_time = xdata_time[i]


#%%

# =============================================================================
# df = pd.DataFrame({'Frequency':[freq], 'Focusing time (99%)':[focus_time],'t_star':[t_star], 'alpha':[alpha], 'R':[R], 'r_squared':r_squared})
# #df.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Resonance freq - Exp 1/Resonance freq - Exp 1.csv', sep=';')
# df.to_csv('/Users/joakimpihl/Desktop/DTU/7. Semester/Bachelorprojekt/Resonance freq - Exp 1/Resonance freq - Exp 1.csv', sep=';')
# =============================================================================
