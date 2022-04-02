#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 20:26:23 2017

@author: nik alexoff

Note: Program written to run on Anaconda on Mac OS X
Note: NDBC buoys return time in GMT. Calling the buoy after 8PM will result in a 'date_validate' error as the buoy believes its 12:XX AM the following day (from Eastern timezone)

To do:  create separate databases for Montauk and Islip
        set up JSON files for .plist / daemon automation
        set up plotting for the 2 databases
        email plots?
        check to make sure that the latest entry doesnt have the same date as what's trying to be added?

"""

#FUNCTIONS#

def check_date(year, month, day):   #check_date function is used to make sure the buoy data that gets added to the dataframe is not old
    current = None
    validate = dt.date(year, month, day)
    if validate==dt.date.today():
        current = True      #this reading is current and should be appended
    else:
        current = False     #this reading is NOT current and should NOT be appended
    return current

def degrees(mwd):   #degrees function is used to convert float values returned by the buoy into more readable string values of the compass rose e.g., N for North, NNE for North-Northeast,etc.
    directions = ['North','North-Northeast','Northeast','East-Northeast','East','East-Southeast','Southeast','South-Southeast','South','South-Southwest','Southwest','West-Southwest','West','West-Northwest','Northwest','North-Northwest']
    if mwd > 348.75 and mwd <= 360 or mwd > 0 and mwd <= 11.25:
        return directions[0]
    elif mwd > 11.25 and mwd <= 33.75:
        return directions[1]
    elif mwd > 33.75 and mwd <= 56.25:
        return directions[2]
    elif mwd > 56.25 and mwd <= 78.75:
        return directions[3]
    elif mwd > 78.75 and mwd <= 101.25:
        return directions[4]
    elif mwd > 101.25 and mwd <= 123.75:
        return directions[5]
    elif mwd > 123.75 and mwd <= 146.25:
        return directions[6]
    elif mwd > 146.25 and mwd <= 168.75:
        return directions[7]
    elif mwd > 168.75 and mwd <= 191.25:
        return directions[8]
    elif mwd > 191.25 and mwd <= 213.75:
        return directions[9]
    elif mwd > 213.75 and mwd <= 236.25:
        return directions[10]
    elif mwd > 236.25 and mwd <= 258.75:
        return directions[11]
    elif mwd > 258.75 and mwd <= 281.25:
        return directions[12]
    elif mwd > 281.25 and mwd <= 303.75:
        return directions[13]
    elif mwd > 303.75 and mwd <= 326.25:
        return directions[14]
    elif mwd > 326.25 and mwd <= 348.75:
        return directions[15]
    return

#IMPORTS#
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


#PROGRAM#
try:
    mtk_url = 'http://www.ndbc.noaa.gov/data/realtime2/44017.txt'   #this is the url of the MONTAUK buoy real-time standard meterological data
    mtk_buoy = pd.read_csv(mtk_url, sep='\s+')     #create dataframe for STATION 44017 (MONTAUK), delimited by 1 OR MORE spaces (due to irregular spacing in txt file)
    mtk_buoy.columns = ['year',                     #rename the dataframe columns to be easily readable...
                        'month',
                        'day',
                        'hour',
                        'minute',
                        'wind direction deg',       #Wind direction (the direction the wind is coming from in degrees clockwise from true N) during the same period used for WSPD.
                        'wind speed m/s',           #Wind speed (m/s) averaged over an eight-minute period for buoys and a two-minute period for land stations. Reported Hourly.
                        'gust speed m/s',           #Peak 5 or 8 second gust speed (m/s) measured during the eight-minute or two-minute period.
                        'wave height m',            #Significant wave height (meters) is calculated as the average of the highest one-third of all of the wave heights during the 20-minute sampling period.
                        'dominant wave period',     #Dominant wave period (seconds) is the period with the maximum wave energy.
                        'avg wave period',          #Average wave period (seconds) of all waves during the 20-minute period.
                        'mean wave direction',      #The direction from which the waves at the dominant period (DPD) are coming. The units are degrees from true North, increasing clockwise, with North as 0 (zero) degrees and East as 90 degrees.
                        'sea level pressure',       #Sea level pressure (hPa)
                        'air temp',                 #Air temperature (Celsius)
                        'sea temp',                 #Sea surface temperature (Celsius)
                        'dewpoint temp',            #Dewpoint temperature taken at the same height as the air temperature measurement
                        'visibility',               #Station visibility (nautical miles). Note that buoy stations are limited to reports from 0 to 1.6 nmi.
                        'pressure tendency',        #Pressure Tendency is the direction (plus or minus) and the amount of pressure change (hPa)for a three hour period ending at the time of observation.
                        'tide']                     #The water level in feet above or below Mean Lower Low Water (The average of the lower low water height of each tidal day observed over the National Tidal Datum Epoch)
    mtk_buoy = mtk_buoy.drop(mtk_buoy.index[0])     #remove the first row of the Dataframe, as the entries are always irrelevant
    mtk_call_check = True                          #set an identifying variable if there was an error in calling the buoy to prevent the rest of the code running
except:
    print("Error - could not reach NDBC Buoy 44017 - Montauk")
    mtk_call_check = False                           #this identifies that there was an error in calling the buoy


if mtk_call_check is True:      #only run the below code if the buoy could be successfully called
    try:
        mtk_buoy = mtk_buoy.head(1)
        pd.to_numeric(mtk_buoy['wave height m'], errors='ignore')
        mtk_buoy['wave height m'] = mtk_buoy['wave height m'].astype(float) * 3.28084   #change the buoy's default reading in meters to imperial (feet)
        mtk_buoy = mtk_buoy.rename(columns={'wave height m': 'wave height'})
        wht_error_mtk = False               #internal variable used to identify issues in code
    except ValueError: #occasionally 'MM' will be returned if buoy sensor malfunctions
        wht_error_mtk = True #in that case, set wave_height_error to True to identify that a reading could not be added to the database

    try:
        mtk_buoy['mean wave direction'] = degrees(float(mtk_buoy['mean wave direction'])) #reassign the DEGREES FROM TRUE NORTH value returned by the buoy as a READABLE LETTER derived from the DEGREES FUNCTION
        mtk_buoy = mtk_buoy.rename(columns={'mean wave direction': 'swell direction'})
        mwd_error_mtk = False         #local identifying variable
    except ValueError:
        mwd_error_mtk = True

    mtk_date = mtk_buoy.iloc[0][['year','month','day']]         #create a series variable of the year, month, day, and hour of latest reading. To be checked against datetime to ensure reading should be added to database
                                                                #alternative method: mtk_date_yr = int(mtk_date[0])
    mtk_date_validate = []                          #create an empty list to be passed through the check_date function
    for i in mtk_date:                              #iterate through the mtk_date Pandas Series (year, month, day)
        mtk_date_validate.append(int(i))            #add each object of series to the validation list as an integer

    if check_date(*mtk_date_validate) is True:      #if the year,month,day of the latest reading passes check_date, append the observation (wave height/period/direction) to the ongoing database
        mtk_data = mtk_buoy[['month','day','year','wave height','dominant wave period','swell direction']].copy()      #create a new dataframe with the relevant data
        mtk_data = mtk_data.head(1)                  #isolate the most recent reading (buoy returns latest on top)
        # with open('DIRECTORY/montauk_data.csv', 'a') as f:  #open the file in append mode as f - replace "DIRECTORY" with relevant directory on machine this runs
            mtk_data.to_csv(f, header=False, index=False)                    #append the dataframe to the CSV file. Header=false ensures column names are not appended, index=False prevents a '1' from being appended as its own column in the csv file
        print('A reading for NDBC Buoy 44017 was added to the Montauk database')
    else:
        print('Could not validate date for NDBC Buoy 44017 - no reading was added to the Montauk database')

### ISLIP ###
### ISLIP ###
### ISLIP ###
### ISLIP ###

try:
    islip_url = 'http://www.ndbc.noaa.gov/data/realtime2/44025.txt'   #this is the url of the ISLIP buoy real-time standard meterological data
    islip_buoy = pd.read_csv(islip_url, sep='\s+')     #create dataframe for STATION 44025 (ISLIP), delimited by 1 OR MORE spaces (due to irregular spacing in txt file)
    islip_buoy.columns = ['year',                     #rename the dataframe columns to be easily readable...
                        'month',
                        'day',
                        'hour',
                        'minute',
                        'wind direction deg',       #Wind direction (the direction the wind is coming from in degrees clockwise from true N) during the same period used for WSPD.
                        'wind speed m/s',           #Wind speed (m/s) averaged over an eight-minute period for buoys and a two-minute period for land stations. Reported Hourly.
                        'gust speed m/s',           #Peak 5 or 8 second gust speed (m/s) measured during the eight-minute or two-minute period.
                        'wave height m',            #Significant wave height (meters) is calculated as the average of the highest one-third of all of the wave heights during the 20-minute sampling period.
                        'dominant wave period',     #Dominant wave period (seconds) is the period with the maximum wave energy.
                        'avg wave period',          #Average wave period (seconds) of all waves during the 20-minute period.
                        'mean wave direction',      #The direction from which the waves at the dominant period (DPD) are coming. The units are degrees from true North, increasing clockwise, with North as 0 (zero) degrees and East as 90 degrees.
                        'sea level pressure',       #Sea level pressure (hPa)
                        'air temp',                 #Air temperature (Celsius)
                        'sea temp',                 #Sea surface temperature (Celsius)
                        'dewpoint temp',            #Dewpoint temperature taken at the same height as the air temperature measurement
                        'visibility',               #Station visibility (nautical miles). Note that buoy stations are limited to reports from 0 to 1.6 nmi.
                        'pressure tendency',        #Pressure Tendency is the direction (plus or minus) and the amount of pressure change (hPa)for a three hour period ending at the time of observation.
                        'tide']                     #The water level in feet above or below Mean Lower Low Water (The average of the lower low water height of each tidal day observed over the National Tidal Datum Epoch)
    islip_buoy = islip_buoy.drop(islip_buoy.index[0])     #remove the first row of the Dataframe, as the entries are always irrelevant
    islip_call_check = True                          #set an identifying variable if there was an error in calling the buoy to prevent the rest of the code running
except:
    print("Error - could not reach NDBC Buoy 44025 - Islip")
    islip_call_check = False                           #this identifies that there was an error in calling the buoy

if islip_call_check is True:        #only run the below code if the buoy could be successfully called
    try:
        islip_buoy = islip_buoy.head(1)
        pd.to_numeric(islip_buoy['wave height m'], errors='ignore')
        islip_buoy['wave height m'] = islip_buoy['wave height m'].astype(float) * 3.28084       #change the buoy's default reading in meters to imperial (feet)
        islip_buoy = islip_buoy.rename(columns={'wave height m': 'wave height ft'})
        wht_error_islip = False
    except ValueError: #occasionally 'MM' will be returned if buoy sensor malfunctions
        wht_error_islip = True #in that case, set wave_height_error to True to identify that a reading could not be added to the database

    try:
        islip_buoy['mean wave direction'] = degrees(float(islip_buoy['mean wave direction'])) #reassign the DEGREES FROM TRUE NORTH value returned by the buoy as a READABLE LETTER derived from the DEGREES FUNCTION
        islip_buoy = islip_buoy.rename(columns={'mean wave direction': 'swell direction'})
        mwd_error_islip = False         #local identifying variable
    except ValueError:
        mwd_error_islip = True

    try:
        islip_buoy['wind direction deg'] = degrees(float(islip_buoy['wind direction deg'])) #reassign the DEGREES FROM TRUE NORTH value returned by the buoy as a READABLE LETTER derived from the DEGREES FUNCTION
        islip_buoy = islip_buoy.rename(columns={'wind direction deg': 'wind direction'})
        wdir_error_islip = False
    except ValueError:
        wdir_error_islip = True

    try:
        islip_buoy['wind speed m/s'] = islip_buoy['wind speed m/s'].astype(float) * 2.23694       #change the buoy's default reading in M/S to imperial (MPH)
        islip_buoy = islip_buoy.rename(columns={'wind speed m/s': 'wind speed mph'})
        wspd_error_islip = False
    except ValueError:
        wspd_error_islip = True

    islip_date = islip_buoy.iloc[0][['year','month','day']]         #create a series variable of the year, month, day, and hour of latest reading. To be checked against datetime to ensure reading should be added to database
                                                                    #alternative method: islip_date_yr = int(islip_date[0])
    islip_date_validate = []                          #create an empty list to be passed through the check_date function
    for i in islip_date:                              #iterate through the islip_date Pandas Series (year, month, day)
        islip_date_validate.append(int(i))            #add each object of series to the validation list as an integer

    if check_date(*islip_date_validate) is True:      #if the year,month,day of the latest reading passes check_date, append the observation (wave height/period/direction) to the ongoing database
        islip_data = islip_buoy[['month','day','year','wave height ft','dominant wave period','swell direction','wind direction','wind speed mph']].copy()      #create a new dataframe with the relevant data
        islip_data = islip_data.head(1)                  #isolate the most recent reading (buoy returns latest on top)
        # with open('/DIRECTORY/islip_data.csv', 'a') as f:  #open the file in append mode as f - replace "DIRECTORY" with relevant directory on machine where this runs
            islip_data.to_csv(f, header=False, index=False)                    #append the dataframe to the CSV file. Header=false ensures column names are not appended, index=False prevents a '1' from being appended as its own column in the csv file
        print('A reading for NDBC Buoy 44025 was added to the Islip database')
    else:
        print('Could not validate date for NDBC Buoy 44025 - no reading was added to the Islip database')

### ISLIP ###
### ISLIP ###
### ISLIP ###
### ISLIP ###

# SET UP DATAFRAMES FOR ANALYSIS
# SET UP DATAFRAMES FOR ANALYSIS

#islip_plot = pd.read_csv('/DIRECTORY/islip_data.csv')  #create a dataframe based on the saved file - replace "DIRECTORY" with relevant directory on machine where this runs
islip_plot= islip_plot.set_index(['month'])     #set the index to the different months captured by the dataframe

ipn = islip_plot.loc[11] #create a new dataframe, ipd (Islip Plot November) using 11 in the index to indentify the month
ipn = ipn.drop('year',axis=1)   #remove the 'year' series from the dataframe as it will not be plotted
ipn = ipn.round(2)  #round all floats to two decimal places

ipd = islip_plot.loc[12] #create a new dataframe, ipd (Islip Plot December) using 12 in the index to indentify the month
ipd = ipd.drop('year',axis=1)   #remove the 'year' series from the dataframe as it will not be plotted
ipd = ipd.round(2)  #round all floats to two decimal places

# SET UP DATAFRAMES FOR ANALYSIS
# SET UP DATAFRAMES FOR ANALYSIS

# NOVEMBER PLOTS
# NOVEMBER PLOTS

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
nov_sdir = ipn['swell direction'].describe()['top'] #SDIR = TOP Swell Direction reading from the month
print('The most frequent swell direction was %s' % (nov_sdir))
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
print('The most frequent wind direction was %s' % (nov_wdir))
print('\n')

# NOVEMBER PLOTS
# NOVEMBER PLOTS


# DECEMBER PLOTS
# DECEMBER PLOTS

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
dec_sdir = ipd['swell direction'].describe()['top'] #SDIR = TOP Swell Direction reading from the month
print('The most frequent swell direction was %s' % (dec_sdir))
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
print('The most frequent wind direction was %s' % (dec_wdir))
print('\n')

# DECEMBER PLOTS
# DECEMBER PLOTS


# VISUALLY COMPARING THE TWO MONTHS - RUN IN JUPYTER NOTEBOOK
# VISUALLY COMPARING THE TWO MONTHS - RUN IN JUPYTER NOTEBOOK

# SUMMARY SUBPLOT COMPARISON
ipn.plot(title='November Summary',  #create a summnary subplot for the month with the three numerical values that have been added to the database
         x='day',
         kind='bar',
         subplots=True,
         figsize=(8,8))

ipd.plot(title='December Summary',  #create a summnary subplot for the month with the three numerical values that have been added to the database
         x='day',
         kind='bar',
         subplots=True,
         figsize=(8,8))

# SUMMARY SWELL HEIGHT COMPARISON
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

# SUMMARY SWELL PERIOD COMPARISON
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

# SUMMARY WIND SPEED COMPARISON
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

# VISUALLY COMPARING THE TWO MONTHS - RUN IN JUPYTER NOTEBOOK
# VISUALLY COMPARING THE TWO MONTHS - RUN IN JUPYTER NOTEBOOK
