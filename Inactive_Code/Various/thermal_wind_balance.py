#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:51:10 2019

@author: aristizabal
"""

#%% User input

temp_matfile = '/Users/aristizabal/Desktop/MARACOOS_project/Maria_scripts/Figures/Model_glider_comp/along_track_temp_prof_ng291_ng467_ng487.mat'
salt_matfile = '/Users/aristizabal/Desktop/MARACOOS_project/Maria_scripts/Figures/Model_glider_comp/along_track_salt_prof_ng291_ng467_ng487.mat'
vel_file = '/Users/aristizabal/Desktop/MARACOOS_project/Maria_scripts/Figures/Model_glider_comp/ng467_depth_aver_vel.mat'
vel_VI_channel_file = '/Users/aristizabal/Desktop/MARACOOS_project/Maria_scripts/Figures/Model_glider_comp/vel_profile_virgin_island_channel_GOFS31.mat'

# Folder where to save figure
folder = '/Users/aristizabal/Desktop/MARACOOS_project/Maria_scripts/Figures/Model_glider_comp/';

date_ini = '17-Jul-2018 00:00:00'
date_end = '17-Sep-2018 00:00:00'

# GOFS 3.1 
catalog31_uv = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_93.0/uv3z';

#%% Modules

import scipy.io as sio 
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from geopy.distance import geodesic
import netCDF4
#from netCDF4 import Dataset
import xarray as xr 

#%% Functions to calculate density

def dens0(s, t):
    s, t = list(map(np.asanyarray, (s, t)))
    T68 = T68conv(t)
    # UNESCO 1983 Eqn.(13) p17.
    b = (8.24493e-1, -4.0899e-3, 7.6438e-5, -8.2467e-7, 5.3875e-9)
    c = (-5.72466e-3, 1.0227e-4, -1.6546e-6)
    d = 4.8314e-4
    return (smow(t) + (b[0] + (b[1] + (b[2] + (b[3] + b[4] * T68) * T68) *
            T68) * T68) * s + (c[0] + (c[1] + c[2] * T68) * T68) * s * s ** 0.5 + d * s ** 2)

def smow(t):
    t = np.asanyarray(t)
    a = (999.842594, 6.793952e-2, -9.095290e-3, 1.001685e-4, -1.120083e-6, 6.536332e-9)
    T68 = T68conv(t)
    return (a[0] + (a[1] + (a[2] + (a[3] + (a[4] + a[5] * T68) * T68) * T68) * T68) * T68)
    
def T68conv(T90):
    T90 = np.asanyarray(T90)
    return T90 * 1.00024

#%% Load all variables

temp_array = sio.loadmat(temp_matfile)
salt_array = sio.loadmat(salt_matfile)
vel_ng467 = sio.loadmat(vel_file)
vel_VI_channel = sio.loadmat(vel_VI_channel_file)

temp_matrix291 = temp_array['tempg_matrix291']
salt_matrix291 = salt_array['saltg_matrix291']
depth_vec291 = temp_array['depthg_vec291']
time_matlab_291 = temp_array['timeg_vec291'][:,0]
lat_vec291 = temp_array['lat291'][:,0]
lon_vec291 = temp_array['lon291'][:,0]

temp_matrix487 = temp_array['tempg_matrix487']
salt_matrix487 = salt_array['saltg_matrix487']
depth_vec487 = temp_array['depthg_vec487']
time_matlab_487 = temp_array['timeg_vec487'][:,0]
lat_vec487 = temp_array['lat487'][:,0]
lon_vec487 = temp_array['lon487'][:,0]

temp_matrix467 = temp_array['tempg_matrix467']
salt_matrix467 = salt_array['saltg_matrix467']
depth_vec467 = temp_array['depthg_vec467']
time_matlab_467 = temp_array['timeg_vec467'][:,0]
lat_vec467 = temp_array['lat467'][:,0]
lon_vec467 = temp_array['lon467'][:,0]

velu467 = vel_ng467['ug'][:,0]
velv467 = vel_ng467['vg'][:,0]
time_matlab_467_vel = vel_ng467['timeg'][:,0]

u31_ng467 = vel_ng467['target_u31']
v31_ng467 = vel_ng467['target_v31']
time31_matlab =  vel_ng467['time31'][:,0]
oktime31 = vel_ng467['oktime31'][:,0]
oklat31_ng467 = vel_ng467['oklat31']

velu31_VI_channel = vel_VI_channel['u31']
lon31_VI_channel = vel_VI_channel['lon_pos'][0]
lat31_VI_channel = vel_VI_channel['lat_pos'][0]
t31_matlab_VI_channel = vel_VI_channel['t31'][:,0]

#%% Changing timestamps to datenum

time_291 = []
time_487 = []
time_467 = []
time_467_vel = []
time31_VI_channel = []
time31 = []
for i in np.arange(len(time_matlab_291)):
    time_291.append(datetime.fromordinal(int(time_matlab_291[i])) + \
        timedelta(days=time_matlab_291[i]%1) - timedelta(days = 366))
for i in np.arange(len(time_matlab_487)):
    time_487.append(datetime.fromordinal(int(time_matlab_487[i])) + \
        timedelta(days=time_matlab_487[i]%1) - timedelta(days = 366))
for i in np.arange(len(time_matlab_467)):
    time_467.append(datetime.fromordinal(int(time_matlab_467[i])) + \
        timedelta(days=time_matlab_467[i]%1) - timedelta(days = 366))
for i in np.arange(len(time_matlab_467_vel)):
    time_467_vel.append(datetime.fromordinal(int(time_matlab_467_vel[i])) + \
        timedelta(days=time_matlab_467_vel[i]%1) - timedelta(days = 366))
for i in np.arange(len(t31_matlab_VI_channel)):
    time31_VI_channel.append(datetime.fromordinal(int(t31_matlab_VI_channel[i])) + \
        timedelta(days=t31_matlab_VI_channel[i]%1) - timedelta(days = 366))   
for i in np.arange(len(time31_matlab)):
    time31.append(datetime.fromordinal(int(time31_matlab[i])) + \
        timedelta(days=time31_matlab[i]%1) - timedelta(days = 366))       
        
time_vec291 = np.asarray(time_291)
time_vec487 = np.asarray(time_487)
time_vec467 = np.asarray(time_467)
time_vec467_vel = np.asarray(time_467_vel)
time31_VI_channel = np.asarray(time31_VI_channel)
time31 = np.asarray(time31)

timestamp_291 = mdates.date2num(time_vec291)
timestamp_487 = mdates.date2num(time_vec487)
timestamp_467 = mdates.date2num(time_vec467)
timestamp_467_vel = mdates.date2num(time_vec467_vel)
timestamp_31_VI_channel = mdates.date2num(time31_VI_channel)
timestamp31 = mdates.date2num(time31)

#%% Choose a common depth for all fields

dmin = np.min([np.max(depth_vec291),np.max(depth_vec487),np.max(depth_vec467)])
okd = np.logical_or(depth_vec291 < dmin,depth_vec291 == dmin)[0,:]
depth_vec = depth_vec291[0,okd]

#%% Interpolate all fields to a common time and depth

timestamp = timestamp_291
time = time_vec291

temp291 = np.empty((len(depth_vec),len(timestamp)))
temp291[:] = np.nan
temp487 = np.empty((len(depth_vec),len(timestamp)))
temp487[:] = np.nan
temp467 = np.empty((len(depth_vec),len(timestamp)))
temp467[:] = np.nan
salt291 = np.empty((len(depth_vec),len(timestamp)))
salt291[:] = np.nan
salt487 = np.empty((len(depth_vec),len(timestamp)))
salt487[:] = np.nan
salt467 = np.empty((len(depth_vec),len(timestamp)))
salt467[:] = np.nan
for z in np.arange(len(depth_vec)):
    temp291[z,:] = np.interp(timestamp,timestamp_291,temp_matrix291[z,:])
    temp487[z,:] = np.interp(timestamp,timestamp_487,temp_matrix487[z,:])
    temp467[z,:] = np.interp(timestamp,timestamp_467,temp_matrix467[z,:])
    salt291[z,:] = np.interp(timestamp,timestamp_291,salt_matrix291[z,:])
    salt487[z,:] = np.interp(timestamp,timestamp_487,salt_matrix487[z,:])
    salt467[z,:] = np.interp(timestamp,timestamp_467,salt_matrix467[z,:])

lat291 = np.interp(timestamp,timestamp_291,lat_vec291)
lat487 = np.interp(timestamp,timestamp_487,lat_vec487)
lat467 = np.interp(timestamp,timestamp_467,lat_vec467)
lon291 = np.interp(timestamp,timestamp_291,lon_vec291)
lon487= np.interp(timestamp,timestamp_487,lon_vec487)
lon467 = np.interp(timestamp,timestamp_467,lon_vec467)

u467 = np.interp(timestamp,timestamp_467_vel,velu467)
v467 = np.interp(timestamp,timestamp_467_vel,velv467)

#%% Reading GOFS3.1 data
'''
GOFS31 = xr.open_dataset(catalog31_uv,decode_times=False)
#GOFS31 = Dataset(catalog31_uv,decode_times=False)

lat31 = GOFS31.variables['lat'][:]
lon31 = GOFS31.variables['lon'][:]
depth31 = GOFS31.variables['depth'][:]
tt31 = GOFS31.variables['time']
#t31 = netCDF4.num2date(tt31[:],tt31.units) 
time31 = netCDF4.num2date(tt31[:],'hours since 2000-01-01 00:00:00') 
'''

# Open the file
import pickle
names = ['lat31','lon31','depth31','time31']
ff = '/Users/aristizabal/Desktop/MARACOOS_project/Maria_scripts/Figures/Model_glider_comp/GOFS31_dimensions.pickle'
myfile = open(ff, 'rb')
for n in names:
    n = pickle.load(myfile)
    
#%%
    
plt.figure()
plt.plot(time_vec467_vel,velu467,'.-')
plt.plot(time,u467,'.-')
     
#%% Get density

rho291 = dens0(salt291, temp291)
rho487 = dens0(salt487, temp487)
rho467 = dens0(salt467, temp467)
   
#%%  Find distance between every glider profile

pos_291 = np.array([lat291,lon291])
pos_487 = np.array([lat487,lon487])

dy = np.empty(pos_291.shape[1])
dy[:] = np.nan
for x in np.arange(pos_291.shape[1]):
    dy[x] = geodesic(pos_291[:,x],pos_487[:,x]).meters
    
#%% Thermal wind balance

g = 9.8 #m/s
f = 0.45 * 10**(-4) # 1/s

rho0291 = np.nanmean(rho291,0)
rho0487 = np.nanmean(rho487,0)
rho0 = (rho0291 + rho0487)/2

drhody_487_291 = (rho291 - rho487)/dy

dudz = - (g/f) * (1/rho0) * drhody_487_291

#%% figure thermal wind balance

plt.figure()
plt.plot(dudz,-depth_vec)
plt.plot(np.zeros(len(depth_vec)),-depth_vec,'-k')

#%% Velocity as a function of z and surface velocity

uz = np.empty((len(depth_vec),len(timestamp)))
uz[:] = np.nan
for t in np.arange(len(timestamp)):
    okz = np.where(np.isfinite(dudz[:,t]))[0]
    for z in np.arange(2,len(okz)):
        uz[z,t] = (g/f) * (1/rho0[t]) * np.trapz(drhody_487_291[okz[0:z],t],depth_vec[okz[0:z]])

uz_depth_mean = np.nanmean(uz,0)

#%% velocity as a function of z

t = 500    
plt.figure()
plt.plot(uz[:,t],-depth_vec,'.-',label='Thermal Wind')
plt.plot(np.ones(len(depth_vec))*uz_depth_mean[t],-depth_vec,'-c',label='Depth Ave thermal wind')
plt.plot(np.ones(len(depth_vec))*u467[t],-depth_vec,'-',label='Depth Ave from ng467')
plt.legend(fontsize=14)
plt.plot(np.zeros(len(depth_vec)),-depth_vec,'-k') 
plt.title('Velocity Profile in the Virgin Island Channel \n on '\
          + str(time[t]),size=20)
plt.ylabel('Depth (m)',size=16)
plt.xlabel('Velocity (m/s)',size=16)

file = 'thermal_wind_calculation_'+ str(date)      
plt.savefig(folder + file\
             ,bbox_inches = 'tight',pad_inches = 0.1) 

#%% velocity as a function of z shifted 

shift = u467 - uz_depth_mean
uz_shift = uz + shift
uz_depth_mean_shift = np.nanmean(uz_shift,0)

plt.figure()
plt.plot(uz_shift,-depth_vec)
plt.plot(np.zeros(len(depth_vec)),-depth_vec,'-k')    

#%% velocity as a function of z shifted

t = 500    
plt.figure()
plt.plot(uz_shift[:,t],-depth_vec,'.-',label='Thermal Wind Shifted')
plt.plot(np.ones(len(depth_vec))*uz_depth_mean_shift[t],-depth_vec,'-c',label='Depth Ave thermal wind shifted')
plt.plot(np.ones(len(depth_vec))*u467[t],-depth_vec,'-',label='Depth Ave from ng467')
plt.legend(fontsize=14)
plt.plot(np.zeros(len(depth_vec)),-depth_vec,'-k') 
plt.title('Velocity Profile in the Virgin Island Channel \n on '\
          + str(time[t]),size=20)
plt.ylabel('Depth (m)',size=16)
plt.xlabel('Velocity (m/s)',size=16)

file = 'thermal_wind_shifted_calculation_'+ str(date)      
plt.savefig(folder + file\
             ,bbox_inches = 'tight',pad_inches = 0.1) 

#%% velocity as a function of z shifted example
date = datetime(2018, 8, 23,12,0,0)
#date = datetime(2018, 7, 30)
#date = datetime(2018, 8, 10)
#date = datetime(2018, 8, 20)


okt1 = np.where(time > date )[0][0]
okt2 = np.where(time31_VI_channel == date)[0][0]
okt3 = np.where(time31[oktime31] == date)[0][0]
okdm = np.logical_or(depth31 < 200, depth31 == 200)

plt.figure()
plt.plot(uz_shift[:,okt1],-depth_vec,'.-',label='Thermal Wind')
#plt.plot(np.ones(len(depth_vec))*uz_depth_mean_shift[t],-depth_vec,'-c',label='Depth Ave shifted')
#plt.plot(np.ones(len(depth_vec))*u467[tg],-depth_vec,'-',label='Depth Ave 467')
plt.plot(velu31_VI_channel[okdm,okt2,0],-1*depth31[okdm],'.-',label='GOFS 3.1, lat= '\
         + str(lat31[lat31_VI_channel[0]][0])[0:5])
plt.plot(u31_ng467[okdm,okt3],-1*depth31[okdm],'.-',label='GOFS 3.1, lat= '\
         + str(lat31[oklat31_ng467[okt2][0]][0])[0:5])
#plt.plot(vel31_VI_channel[okdm,okt,1],-1*depth31[okdm],label='GOFS 3.1, lat= '\
#         + str(lat31[lat31_VI_channel[0][1]][0])[0:5])
#plt.plot(vel31_VI_channel[okdm,okt,2],-1*depth31[okdm],label='GOFS 3.1, lat= '\
#         + str(lat31[lat31_VI_channel[0][2]][0])[0:5])
#plt.plot(np.ones(len(depth31[okdm]))*np.nanmean(vel31_VI_channel[okdm,okt,0],0),-1*depth31[okdm],label='mean GOFS 3.1')
plt.legend(fontsize=14)
plt.plot(np.zeros(len(depth_vec)),-depth_vec,'--k') 
plt.title('Velocity Profile in the Virgin Island Channel \n on '\
          + str(date),size=20)
plt.ylabel('Depth (m)',size=16)
plt.xlabel('Velocity (m/s)',size=16)

file = 'thermal_wind_vs_GOFS31_VI_channel_'+ str(date)      
plt.savefig(folder + file\
             ,bbox_inches = 'tight',pad_inches = 0.1) 

