#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 16:32:46 2017

@author: nalexoff
"""

import pandas as pd
import matplotlib.pyplot as plt

# SET UP DATAFRAMES FOR ANALYSIS
#islip_plot = pd.read_csv('DIRECTORY.csv')  #create a dataframe based on the saved file - replace "DIRECTORY" with relevant directory where file is saved 
islip_plot= islip_plot.set_index(['month'])     #set the index to the different months captured by the dataframe

ipn = islip_plot.loc[11] #create a new dataframe, ipd (Islip Plot November) using 11 in the index to indentify the month
ipn = ipn.drop('year',axis=1)   #remove the 'year' series from the dataframe as it will not be plotted
ipn = ipn.round(2)  #round all floats to two decimal places

ipd = islip_plot.loc[12] #create a new dataframe, ipd (Islip Plot December) using 12 in the index to indentify the month
ipd = ipd.drop('year',axis=1)   #remove the 'year' series from the dataframe as it will not be plotted
ipd = ipd.round(2)  #round all floats to two decimal places
# SET UP DATAFRAMES FOR ANALYSIS

# NOVEMBER
ipn.plot(title='November Summary',  #create a summnary subplot for the month with the three numerical values that have been added to the database
         x='day',
         kind='bar',
         subplots=True,
         figsize=(8,8))

ipn.plot(kind='bar',    #create a monthly 'swell height ft' plot by day of month
         x='day',
         y='swell height ft')

nov_shmean = ipn['swell height ft'].mean()    #smh = SWELL HEIGHT MEAN
nov_shmin = ipn['swell height ft'].min()   #SHMIN = SWELL HEIGHT MIN
nov_shmax = ipn['swell height ft'].max()   #SHMAX = SWELL HEIGHT MAX

print('\n')
print('Average swell height was %s ft' % (nov_shmean))
print('\n')
print('The low swell height for the month was %s ft while the high was %s ft' % (nov_shmin,nov_shmax))
print('\n')

ipn.plot(kind='bar',    #create a monthly 'swell period sec' plot by day of month
         x='day',
         y='swell period sec',
         color = 'orange')


nov_spmean = ipn['swell period sec'].mean()    #spmean = SWELL PERIOD MEAN
nov_spmin = ipn['swell period sec'].min()   #SpMIN = SWELL PERIOD MIN
nov_spmax = ipn['swell period sec'].max()   #SpMAX = SWELL PERIOD MAX

print('\n')
print('Average swell period was %s sec' % (nov_spmean))
print('\n')
print('The shortest swell period for the month was %s sec while the longest was %s sec' % (nov_spmin,nov_spmax))
print('\n')

nov_sdir = ipn['swell direction'].describe()['top'] #SDIR = TOP Swell Direction reading from the month
print('\n')
print('The most frequent swell direction was %s' % (nov_sdir))
print('\n')


ipn.plot(kind='bar',    #create a monthly 'wind speed mph' plot by day of month
         x='day',
         y='wind speed mph',
         color = 'green')

nov_wsmean = ipn['wind speed mph'].mean()    #wsmean = wind speed mph MEAN
nov_wsmin = ipn['wind speed mph'].min()   #wsMIN = wind speed mph MIN
nov_wsmax = ipn['wind speed mph'].max()   #wsMAX = wind speed mph MAX

print('\n')
print('Average wind speed was %s mph' % (nov_wsmean))
print('\n')
print('The low wind speed for the month was %s mph while the high was %s mph' % (nov_wsmin,nov_wsmax))
print('\n')

nov_wdir = ipn['wind direction'].describe()['top'] #WDIR = TOP WIND Direction reading from the month
print('\n')
print('The most frequent wind direction was %s' % (nov_wdir))
print('\n')
# NOVEMBER


# DECEMBER 
ipd.plot(title='December Summary',  #create a summnary subplot for the month with the three numerical values that have been added to the database
         x='day',
         kind='bar',
         subplots=True,
         figsize=(8,8))

ipd.plot(kind='bar',    #create a monthly 'swell height ft' plot by day of month
         x='day',
         y='swell height ft')

dec_shmean = ipd['swell height ft'].mean()    #smh = SWELL HEIGHT MEAN
dec_shmin = ipd['swell height ft'].min()   #SHMIN = SWELL HEIGHT MIN
dec_shmax = ipd['swell height ft'].max()   #SHMAX = SWELL HEIGHT MAX

print('\n')
print('Average swell height was %s ft' % (dec_shmean))
print('\n')
print('The low swell height for the month was %s ft while the high was %s ft' % (dec_shmin,dec_shmax))
print('\n')

ipd.plot(kind='bar',    #create a monthly 'swell period sec' plot by day of month
         x='day',
         y='swell period sec',
         color = 'orange')


dec_spmean = ipd['swell period sec'].mean()    #spmean = SWELL PERIOD MEAN
dec_spmin = ipd['swell period sec'].min()   #SpMIN = SWELL PERIOD MIN
dec_spmax = ipd['swell period sec'].max()   #SpMAX = SWELL PERIOD MAX

print('\n')
print('Average swell period was %s sec' % (dec_spmean))
print('\n')
print('The shortest swell period for the month was %s sec while the longest was %s sec' % (dec_spmin,dec_spmax))
print('\n')

dec_sdir = ipd['swell direction'].describe()['top'] #SDIR = TOP Swell Direction reading from the month
print('\n')
print('The most frequent swell direction was %s' % (dec_sdir))
print('\n')


ipd.plot(kind='bar',    #create a monthly 'wind speed mph' plot by day of month
         x='day',
         y='wind speed mph',
         color = 'green')

dec_wsmean = ipd['wind speed mph'].mean()    #wsmean = wind speed mph MEAN
dec_wsmin = ipd['wind speed mph'].min()   #wsMIN = wind speed mph MIN
dec_wsmax = ipd['wind speed mph'].max()   #wsMAX = wind speed mph MAX

print('\n')
print('Average wind speed was %s mph' % (dec_wsmean))
print('\n')
print('The low wind speed for the month was %s mph while the high was %s mph' % (dec_wsmin,dec_wsmax))
print('\n')

dec_wdir = ipd['wind direction'].describe()['top'] #WDIR = TOP WIND Direction reading from the month
print('\n')
print('The most frequent wind direction was %s' % (dec_wdir))
print('\n')
# DECEMBER

# COMPARING THE TWO MONTHS
nov_sh = pd.Series([nov_shmean,nov_shmin,nov_shmax])    #november swell height series
dec_sh = pd.Series([dec_shmean,dec_shmin,dec_shmax])    #december swell height series
sh_compare = pd.DataFrame(data=[nov_sh,dec_sh])
sh_compare.columns=['swell height average','swell height min','swell height max']
sh_compare = sh_compare.T
fig, ax = plt.subplots()
sh_compare.plot(ax=ax,kind='bar')
ax.set_title('Swell Height Comparison')
ax.set_ylabel('Feet')
ax.legend(['November','December'])
#sh_compare.plot(kind='bar')

nov_sp = pd.Series([nov_spmean,nov_spmin,nov_spmax])    #november swell period series
dec_sp = pd.Series([dec_spmean,dec_spmin,dec_spmax])    #december swell period series
sp_compare = pd.DataFrame(data=[nov_sp,dec_sp])
sp_compare.columns=['swell period average','swell period short','swell period long']
sp_compare = sp_compare.T
fig, ax = plt.subplots()
sp_compare.plot(ax=ax,kind='bar')
ax.set_title('Swell Period Comparison')
ax.set_ylabel('Seconds')
ax.legend(['November','December'])


nov_w = pd.Series([nov_wsmean,nov_wsmin,nov_wsmax])    #november wind series
dec_w = pd.Series([dec_wsmean,dec_wsmin,dec_wsmax])    #december wind series
w_compare = pd.DataFrame(data=[nov_w,dec_w])
w_compare.columns=['wind speed average','wind speed min','wind speed max']
w_compare = w_compare.T
fig, ax = plt.subplots()
w_compare.plot(ax=ax,kind='bar')
ax.set_title('Wind Speed Comparison')
ax.set_ylabel('MPH')
ax.legend(['November','December'])
# COMPARING THE TWO MONTHS
