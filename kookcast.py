#API KEYS:
#WUNDERGROUND: (API KEY to WUNDERGROUND.COM REQUIRED) 

#my functions##my functions##my functions##my functions##my functions##my functions##my functions#
#my functions##my functions##my functions##my functions##my functions##my functions##my functions#


def mtk_buoy_data(): #mtk = mountauk buoy data
    url = "http://www.ndbc.noaa.gov/data/realtime2/44017.txt" #44017 is designatior for NDBC's Montauk (MTK) buoy
    filename = wget.download(url)
    return

def islip_buoy_data(): #mtk = mountauk buoy data
    url = "http://www.ndbc.noaa.gov/data/realtime2/44025.txt" #44025 is designatior for NDBC's Islip (ISLIP) buoy
    filename = wget.download(url)
    return

def delete_ndbc_files():
    #os.unlink("/DIRECTORY/44017.txt") Replace "DIRECTORY" with relevant location on machine this is running
    #os.unlink("/DIRECTORY/44025.txt") Replace "DIRECTORY" with relevant location on machine this is running
    return


#my program##my program##my program##my program##my program##my program##my program##my program#
#my program##my program##my program##my program##my program##my program##my program##my program#

import wget #import wget, preferred method for NDBC (NOAA) to access realtime buoy data files
import smtplib #import smtplib for sending emails
import datetime
import time
import os
from bs4 import BeautifulSoup #used to pull surfline forecast
import json
import requests

# / DOWNLOAD NDBC REAL-TIME DATA FOR MONTAUK AND ISLIP
try:
    mtk_buoy_data()
    islip_buoy_data()
    print()
    print("Real-time NDBC data downloaded")
except:
    print()
    print("Error downloading NDBC data")
#DOWNLOAD NDBC REAL-TIME DATA FOR MONTAUK AND ISLIP /

# / MONTAUK VARIABLE-SETTING
mtk_file = open("44017.txt", "r") #open the file downloaded by mtk_buoy_data
mtk_file_contents = mtk_file.readlines() #read the file and return it as a list
mtk_file.close() #close the file
mtk_data_all = mtk_file_contents[2] #isolate the most recent data from the NDBC buoy (3rd line from top in downloaded file)
mtk_data_all_list = mtk_data_all.split(" ") #split the string into a list of individual elemeents, separated by " "
mtk_data_all_list = list(filter(None, mtk_data_all_list)) #remove all the empty (" ") elements returned by the buoy to allow for consistent indexing
try:
    mtk_wvht = float(mtk_data_all_list[8]) #set a variable for the WAVE HEIGHT IN METERS #go to 9th element in the mtk_data_all_list and set a float variable
    mtk_wvht = float(mtk_wvht * 3.28084) #convert to WAVE HEIGHT IN FEET
except ValueError: #occasionally 'MM' will be returned if buoy sensor malfunctions
    mtk_wvht = None #in that case, set mtk_wvht to None to identify that it needs to be a string in the email body
try:
    mtk_dpd = float(mtk_data_all_list[9]) #set a variable for the DOMINANT SWELL PERIOD IN SECONDS
except ValueError:
    mtk_dpd = None
try:
    mtk_mwd = float(mtk_data_all_list[11]) #set a variable for the DOMINANT SWELL DIRECTION IN DEGREES FROM TURE NORTH (N=0, E=90, etc.)
    if mtk_mwd > 348.75 and mtk_mwd <= 11.25:
        mtk_mwd = str("N")
    elif mtk_mwd > 11.25 and mtk_mwd <= 33.75:
        mtk_mwd = str("NNE")
    elif mtk_mwd > 33.75 and mtk_mwd <= 56.25:
        mtk_mwd = str("NE")
    elif mtk_mwd > 56.25 and mtk_mwd <= 78.75:
        mtk_mwd = str("ENE")
    elif mtk_mwd > 78.75 and mtk_mwd <= 101.25:
        mtk_mwd = str("E")
    elif mtk_mwd > 101.25 and mtk_mwd <= 123.75:
        mtk_mwd = str("ESE")
    elif mtk_mwd > 123.75 and mtk_mwd <= 146.25:
        mtk_mwd = str("SE")
    elif mtk_mwd > 146.25 and mtk_mwd <= 168.75:
        mtk_mwd = str("SSE")
    elif mtk_mwd > 168.75 and mtk_mwd <= 191.25:
        mtk_mwd = str("S")
    elif mtk_mwd > 191.25 and mtk_mwd <= 213.75:
        mtk_mwd = str("SSW")
    elif mtk_mwd > 213.75 and mtk_mwd <= 236.25:
        mtk_mwd = str("SW")
    elif mtk_mwd > 236.25 and mtk_mwd <= 258.75:
        mtk_mwd = str("WSW")
    elif mtk_mwd > 258.75 and mtk_mwd <= 281.25:
        mtk_mwd = str("W")
    elif mtk_mwd > 281.25 and mtk_mwd <= 303.75:
        mtk_mwd = str("WNW")
    elif mtk_mwd > 303.75 and mtk_mwd <= 326.25:
        mtk_mwd = str("NW")
    elif mtk_mwd > 326.25 and mtk_mwd <= 348.75:
        mtk_mwd = str("NNW")
except ValueError:
    mtk_mwd = None
#MONTAUK VARIABLE-SETTING /

# / ISLIP VARIABLE-SETTING
islip_file = open("44025.txt", "r") #see above commenting for mtk_file
islip_file_contents = islip_file.readlines()
islip_file.close()
islip_data_all = islip_file_contents[2]
islip_data_all_list = islip_data_all.split(" ")
islip_data_all_list = list(filter(None, islip_data_all_list))
try:
    islip_wvht = float(islip_data_all_list[8]) #see above commenting for mtk_wvht
    islip_wvht = float(islip_wvht * 3.28084)
except ValueError:
    islip_wvht = None
try:
    islip_dpd = float(islip_data_all_list[9]) #see above commenting for mtk_wvht
except ValueError:
    islip_dpd = None
try:
    islip_mwd = float(islip_data_all_list[11]) #see above commenting for mtk_wvht
    if islip_mwd > 348.75 and islip_mwd <= 11.25:
        islip_mwd = str("N")
    elif islip_mwd > 11.25 and islip_mwd <= 33.75:
        islip_mwd = str("NNE")
    elif islip_mwd > 33.75 and islip_mwd <= 56.25:
        islip_mwd = str("NE")
    elif islip_mwd > 56.25 and islip_mwd <= 78.75:
        islip_mwd = str("ENE")
    elif islip_mwd > 78.75 and islip_mwd <= 101.25:
        islip_mwd = str("E")
    elif islip_mwd > 101.25 and islip_mwd <= 123.75:
        islip_mwd = str("ESE")
    elif islip_mwd > 123.75 and islip_mwd <= 146.25:
        islip_mwd = str("SE")
    elif islip_mwd > 146.25 and islip_mwd <= 168.75:
        islip_mwd = str("SSE")
    elif islip_mwd > 168.75 and islip_mwd <= 191.25:
        islip_mwd = str("S")
    elif islip_mwd > 191.25 and islip_mwd <= 213.75:
        islip_mwd = str("SSW")
    elif islip_mwd > 213.75 and islip_mwd <= 236.25:
        islip_mwd = str("SW")
    elif islip_mwd > 236.25 and islip_mwd <= 258.75:
        islip_mwd = str("WSW")
    elif islip_mwd > 258.75 and islip_mwd <= 281.25:
        islip_mwd = str("W")
    elif islip_mwd > 281.25 and islip_mwd <= 303.75:
        islip_mwd = str("WNW")
    elif islip_mwd > 303.75 and islip_mwd <= 326.25:
        islip_mwd = str("NW")
    elif islip_mwd > 326.25 and islip_mwd <= 348.75:
        islip_mwd = str("NNW")
except ValueError:
    islip_mwd = None
try:
    islip_wdir = float(islip_data_all_list[5]) #set a variable for WIND DIRECTION (the direction the wind is coming from in degrees clockwise from true N) during the same period used for wspd
    if islip_wdir > 348.75 and islip_wdir <= 11.25:
        islip_wdir = str("N")
    elif islip_wdir > 11.25 and islip_wdir <= 33.75:
        islip_wdir = str("NNE")
    elif islip_wdir > 33.75 and islip_wdir <= 56.25:
        islip_wdir = str("NE")
    elif islip_wdir > 56.25 and islip_wdir <= 78.75:
        islip_wdir = str("ENE")
    elif islip_wdir > 78.75 and islip_wdir <= 101.25:
        islip_wdir = str("E")
    elif islip_wdir > 101.25 and islip_wdir <= 123.75:
        islip_wdir = str("ESE")
    elif islip_wdir > 123.75 and islip_wdir <= 146.25:
        islip_wdir = str("SE")
    elif islip_wdir > 146.25 and islip_wdir <= 168.75:
        islip_wdir = str("SSE")
    elif islip_wdir > 168.75 and islip_wdir <= 191.25:
        islip_wdir = str("S")
    elif islip_wdir > 191.25 and islip_wdir <= 213.75:
        islip_wdir = str("SSW")
    elif islip_wdir > 213.75 and islip_wdir <= 236.25:
        islip_wdir = str("SW")
    elif islip_wdir > 236.25 and islip_wdir <= 258.75:
        islip_wdir = str("WSW")
    elif islip_wdir > 258.75 and islip_wdir <= 281.25:
        islip_wdir = str("W")
    elif islip_wdir > 281.25 and islip_wdir <= 303.75:
        islip_wdir = str("WNW")
    elif islip_wdir > 303.75 and islip_wdir <= 326.25:
        islip_wdir = str("NW")
    elif islip_wdir > 326.25 and islip_wdir <= 348.75:
        islip_wdir = str("NNW")
except ValueError:
    islip_wdir = None
try:
    islip_wspd = float(islip_data_all_list[6]) #set a variable for the WIND SPEED (m/s) averaged over an eight-minute period for buoys
    islip_wspd = (islip_wspd * 2.23694) #Convert to MPH from m/s
except ValueError:
    islip_wspd = None
#ISLIP VARIABLE-SETTING /

# / IF MTK/ISLIP BUOYS RETURNED 'MM' STRING INSTEAD OF AN INTEGER, SET VARIABLE TO DATA UNAVAILABLE STRING
if mtk_wvht == None:
    mtk_wvht = "Data unavailable at this time."
if mtk_dpd == None:
    mtk_dpd = "Data unavailable at this time."
if mtk_mwd == None:
    mtk_mwd = "Data unavailable at this time."

if islip_wvht == None:
    islip_wvht = "Data unavailable at this time."
if islip_dpd == None:
    islip_dpd = "Data unavailable at this time."
if islip_mwd == None:
    islip_mwd = "Data unavailable at this time."
if islip_wdir == None:
    islip_wdir = "Data unavailable at this time."
if islip_wspd == None:
    islip_wspd = "Data unavailable at this time."
#IF MTK/ISLIP BUOYS RETURNED 'MM' STRING INSTEAD OF AN INTEGER, SET VARIABLE TO DATA UNAVAILABLE STRING /

#/ PULLING THE SURFLINE FORECAST
reply = requests.get("http://www.surfline.com/surf-forecasts/long-island/suffolk-county_2146/")
html = reply.text #contents of the request in unicode
soup = BeautifulSoup(html,"html.parser") #using this function, passing it as an argument and then the string as a second argument; second string allows it to use different PARSERS that make sense of different blocks of text
results_str = soup.find(id="observed_component").text
results_str = results_str.split("\n") #split the string into a list of individual elemeents, separated by " "
results_str = list(filter(None, results_str)) #remove all the empty (" ") elements to allow for consistent indexing
today = str(results_str[0]) #day of week and MONTH:DATE
tomorrow = str(results_str[7])
day_after = str(results_str[14])
today_qual = str(results_str[1]) #qualitative forecast for today (e.g., Poor)
tomorrow_qual = str(results_str[8])
day_after_qual = str(results_str[15])
today_quant = str(results_str[4]) #quantitative forecast for today (e.g., 2-3FT)
tomorrow_quant = str(results_str[11])
day_after_quant = str(results_str[18])
today_words = str(results_str[6]) #today's forecast in prose (e.g., Small S windwswell and SE swell)
tomorrow_words = str(results_str[13])
day_after_words = str(results_str[20])
#PULLING THE SURFLINE FORECAST /

#PINGING THE WUNDERGROUND API /
#url = "http://api.wunderground.com/api/APIKEY/hourly10day/q/11977.json" Replace "APIKEY" with key for wunderground.com
try:
    response = requests.get(url)
    print("Wunderground API Hourly 10-day request successful")
    print()
except:
    print("couldn't run requests.get(), some exception got thrown")
data = json.loads(response.text) #feed the answer into JSON

#ESTABLISH VARIABLES FOR WIND SPD/DIR CONDITIONS in 4-HOUR BLOCKS FROM REQUEST
wu_wspd1 = data["hourly_forecast"][0]["wspd"]["english"]
wu_wdir1 = data["hourly_forecast"][0]["wdir"]["dir"]
wu_hour1 = data["hourly_forecast"][0]["FCTTIME"]["civil"]

wu_wspd2 = data["hourly_forecast"][3]["wspd"]["english"]
wu_wdir2 = data["hourly_forecast"][3]["wdir"]["dir"]
wu_hour2 = data["hourly_forecast"][3]["FCTTIME"]["civil"]

wu_wspd3 = data["hourly_forecast"][6]["wspd"]["english"]
wu_wdir3 = data["hourly_forecast"][6]["wdir"]["dir"]
wu_hour3 = data["hourly_forecast"][6]["FCTTIME"]["civil"]

wu_wspd4 = data["hourly_forecast"][9]["wspd"]["english"]
wu_wdir4 = data["hourly_forecast"][9]["wdir"]["dir"]
wu_hour4 = data["hourly_forecast"][9]["FCTTIME"]["civil"]

wu_wspd5 = data["hourly_forecast"][12]["wspd"]["english"]
wu_wdir5 = data["hourly_forecast"][12]["wdir"]["dir"]
wu_hour5 = data["hourly_forecast"][12]["FCTTIME"]["civil"]

wu_wspd6 = data["hourly_forecast"][15]["wspd"]["english"]
wu_wdir6 = data["hourly_forecast"][15]["wdir"]["dir"]
wu_hour6 = data["hourly_forecast"][15]["FCTTIME"]["civil"]

wu_wspd7 = data["hourly_forecast"][18]["wspd"]["english"]
wu_wdir7 = data["hourly_forecast"][18]["wdir"]["dir"]
wu_hour7 = data["hourly_forecast"][18]["FCTTIME"]["civil"]

wu_wspd8 = data["hourly_forecast"][21]["wspd"]["english"]
wu_wdir8 = data["hourly_forecast"][21]["wdir"]["dir"]
wu_hour8 = data["hourly_forecast"][21]["FCTTIME"]["civil"]

wu_wspd9 = data["hourly_forecast"][24]["wspd"]["english"]
wu_wdir9 = data["hourly_forecast"][24]["wdir"]["dir"]
wu_hour9 = data["hourly_forecast"][24]["FCTTIME"]["civil"]

#GETTING SUNRISE AND SUNSET DATA
#url = "http://api.wunderground.com/api/APIKEY/astronomy/q/11977.json" Replace "APIKEY" with key for wunderground.com
try:
    response = requests.get(url)
    print("Wunderground API Astronomy request successful")
    print()
except:
    print("couldn't run requests.get(), some exception got thrown")
data = json.loads(response.text) #feed the answer into JSON
sunrise_hour = data["sun_phase"]["sunrise"]["hour"]
sunrise_min = data["sun_phase"]["sunrise"]["minute"]
sunset_hour = data["sun_phase"]["sunset"]["hour"]
sunset_min = data["sun_phase"]["sunset"]["minute"]
#/ PINGING THE WUNDERGROUND API

#/ PINGING THE NOAA API FOR TIDE
noaatoday = datetime.date.today().strftime('%Y%m%d')
noaaaftertomorrow = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%Y%m%d')
params = {'product': 'predictions', 'application': 'NOS.COOPS.TAC.WL', 'begin_date': noaatoday, 'end_date': noaaaftertomorrow, 'datum': 'MLLW', 'station': '8512354', 'time_zone': 'lst_ldt', 'units': 'english', 'interval': 'hilo', 'format': 'json'}
try:
    response = requests.get('https://tidesandcurrents.noaa.gov/api/datagetter', params=params)
    print("NOAA tide Prediction retrieval successful")
except:
    print("Error getting NOAA tide prediction")
data = json.loads(response.text) #feed the answer into JSON
today_daytime0 = data["predictions"][0]['t']
today_tide_type0 = data["predictions"][0]['type']
today_daytime1 = data["predictions"][1]['t']
today_tide_type1 = data["predictions"][1]['type']
today_daytime2 = data["predictions"][2]['t']
today_tide_type2 = data["predictions"][2]['type']
today_daytime3 = data["predictions"][3]['t']
today_tide_type3 = data["predictions"][3]['type']
tom_daytime0 = data["predictions"][4]['t']
tom_tide_type0 = data["predictions"][4]['type']
tom_daytime1 = data["predictions"][5]['t']
tom_tide_type1 = data["predictions"][5]['type']
tom_daytime2 = data["predictions"][6]['t']
tom_tide_type2 = data["predictions"][6]['type']
tom_daytime3 = data["predictions"][7]['t']
tom_tide_type3 = data["predictions"][7]['type']
dayafter_daytime0 = data["predictions"][8]['t']
dayafter_tide_type0 = data["predictions"][8]['type']
dayafter_daytime1 = data["predictions"][9]['t']
dayafter_tide_type1 = data["predictions"][9]['type']
dayafter_daytime2 = data["predictions"][10]['t']
dayafter_tide_type2 = data["predictions"][10]['type']
try:
    dayafter_daytime3 = data["predictions"][11]['t']
except:
    dayafter_daytime3 = str("Data unavailable - list index out of range")
try:
    dayafter_tide_type3 = data["predictions"][11]['type']
except:
    dayafter_tide_type3 = str("Data unavailable - list index out of range")
#PINGING THE NOAA API FOR TIDE DATA /


# / SCRAPING SWELLINFO TO GET FORECAST
reply = requests.get("https://www.swellinfo.com/surf-forecast/southampton-new-york")
html = reply.text #contents of the request in unicode
soup = BeautifulSoup(html,"html.parser") #using this function, passing it as an argument and then the string as a second argument; second string allows it to use different PARSERS that make sense of different blocks of text
tables = soup.findChildren('table')

today_6am = []
today_6am_detail = tables[4]
rows = today_6am_detail.findChildren(['th', 'tr']) # You can find children with multiple tags by passing a list of strings
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        today_6am.append(value)
        today_6am = list(filter(None, today_6am)) #remove all the empty (" ") elements to allow for consistent indexing
today_6am_time = today_6am[0]
today_6am_wind = today_6am[1]
today_6am_swelldirection = today_6am[2]
today_6am_swell = today_6am[3]

today_9am = []
today_9am_detail = tables[5]
rows = today_9am_detail.findChildren(['th', 'tr'])
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        today_9am.append(value)
        today_9am = list(filter(None, today_9am))
today_9am_time = today_9am[0]
today_9am_wind = today_9am[1]
today_9am_swelldirection = today_9am[2]
today_9am_swell = today_9am[3]

today_12pm = []
today_12pm_detail = tables[6]
rows = today_12pm_detail.findChildren(['th', 'tr'])
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        today_12pm.append(value)
        today_12pm = list(filter(None, today_12pm))
today_12pm_time = today_12pm[0]
today_12pm_wind = today_12pm[1]
today_12pm_swelldirection = today_12pm[2]
today_12pm_swell = today_12pm[3]

today_3pm = []
today_3pm_detail = tables[7]
rows = today_3pm_detail.findChildren(['th', 'tr'])
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        today_3pm.append(value)
        today_3pm = list(filter(None, today_3pm))
today_3pm_time = today_3pm[0]
today_3pm_wind = today_3pm[1]
today_3pm_swelldirection = today_3pm[2]
today_3pm_swell = today_3pm[3]

today_6pm = []
today_6pm_detail = tables[8]
rows = today_6pm_detail.findChildren(['th', 'tr'])
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        today_6pm.append(value)
        today_6pm = list(filter(None, today_6pm))
today_6pm_time = today_6pm[0]
today_6pm_wind = today_6pm[1]
today_6pm_swelldirection = today_6pm[2]
today_6pm_swell = today_6pm[3]

next_6am = []
next_6am_detail = tables[14]
rows = next_6am_detail.findChildren(['th', 'tr'])
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        next_6am.append(value)
        next_6am = list(filter(None, next_6am))
next_6am_time = next_6am[0]
next_6am_wind = next_6am[1]
next_6am_swelldirection = next_6am[2]
next_6am_swell = next_6am[3]

next2_6am = []
next2_6am_detail = tables[24]
rows = next2_6am_detail.findChildren(['th', 'tr'])
for row in rows:
    cells = row.findChildren('td')
    for cell in cells:
        value = cell.string
        next2_6am.append(value)
        next2_6am = list(filter(None, next2_6am))
next2_6am_time = next2_6am[0]
next2_6am_wind = next2_6am[1]
next2_6am_swelldirection = next2_6am[2]
next2_6am_swell = next2_6am[3]
#SCRAPING SWELLINFO TO GET FORECAST /


# / CREATING THE EMAIL VARIABLES
#MAIN HEADERS
this_moment = datetime.datetime.now()
main_header = "Your kookcast for " + datetime.datetime.strftime(this_moment, "%m/%d") + ", generated at " + datetime.datetime.now().strftime("%-I:%M%p") + "\n" + "\n"
now = "====== WHAT'S HAPPENING TODAY? ======" + "\n" + "\n"
reports = "=== REPORTS ===" + "\n" + "\n"
surfline = "Surfline's Suffolk County Forecast:" + "\n" + "\n"
swellinfo = "SwellInfo's Southampton Forecast:" + "\n" + "\n"
ndbc_swell_header = "Real-time NDBC swell data: " + "\n" + "\n"
wunderground = "Wunderground wind outlook:" + "\n" + "\n"
ndbc_wind_header = "Real-time NDBC wind data: " + "\n" + "\n"
noaa = "Tidal predictions (Shinnecock Inlet): "+ "\n" + "\n"
sun = "Sunrise and sunset:" + "\n" + "\n"
later = "====== WHAT'S HAPPENING IN THE NEAR FUTURE? ======" + "\n" + "\n"
swell = "=== SWELL ===" + "\n" + "\n"
wind = "=== WIND ===" + "\n" + "\n"
tide = "=== TIDE ===" + "\n" + "\n"
light = "=== SUN ===" + "\n" + "\n"
surfline_swell_combined = "Combined Surfline & SwellInfo Forecast:" + "\n" + "\n"
#WHAT'S HAPPENING NOW?#WHAT'S HAPPENING NOW?#WHAT'S HAPPENING NOW?#WHAT'S HAPPENING NOW?
#WHAT'S HAPPENING NOW?#WHAT'S HAPPENING NOW?#WHAT'S HAPPENING NOW?#WHAT'S HAPPENING NOW?

#REPORTS
#REPORTS
#SURFLINE VARIABLES
surfline_today = "%s: %s, %s. %s" % (today, today_qual, today_quant, today_words) + "\n" + "\n"

#SWELLINFO VARIABLES
swellinfo_today1 = "%s: Swell: %s, Swell Direction: %s, Wind: %s" % (today_6am_time, today_6am_swell, today_6am_swelldirection, today_6am_wind) + "\n"
swellinfo_today2 = "%s: Swell: %s, Swell Direction: %s, Wind: %s" % (today_9am_time, today_9am_swell, today_9am_swelldirection, today_9am_wind) + "\n"
swellinfo_today3 = "%s: Swell: %s, Swell Direction: %s, Wind: %s" % (today_12pm_time, today_12pm_swell, today_12pm_swelldirection, today_12pm_wind) + "\n"
swellinfo_today4 = "%s: Swell: %s, Swell Direction: %s, Wind: %s" % (today_3pm_time, today_3pm_swell, today_3pm_swelldirection, today_3pm_wind) + "\n"
swellinfo_today5 = "%s: Swell: %s, Swell Direction: %s, Wind: %s" % (today_6pm_time, today_6pm_swell, today_6pm_swelldirection, today_6pm_wind) + "\n" + "\n"

#SWELL
#SWELL
#NDBC VARIABLES
try: #Either store each variable as a string with an integer or the string that says "data unavailable at this time"
    mtk_wvht_body = "Montauk Wave Height: %2.1f ft " % (mtk_wvht) + "\n"
except:
    mtk_wvht_body = "Montauk Wave Height: %s  " % (mtk_wvht) + "\n"
try:
    mtk_dpd_body = "Montauk Swell Period: %i sec " % (mtk_dpd) + "\n"
except:
    mtk_wvht_body = "Montauk Swell Period: %s " % (mtk_dpd) + "\n"
try:
    mtk_mwd_body = "Montauk Swell Direction: %s " % (mtk_mwd) + "\n"
except:
    mtk_mwd_body = "Montauk Swell Direction: %s " % (mtk_mwd) + "\n"
try:
    islip_wvht_body = "Islip Wave Height: %2.1f ft " % (islip_wvht) + "\n"
except:
    islip_wvht_body = "Islip Wave Height: %s " % (islip_wvht) + "\n"
try:
    islip_dpd_body = "Islip Swell Period: %i sec " % (islip_dpd) + "\n"
except:
    islip_dpd_body = "Islip Swell Period: %s " % (islip_dpd) + "\n"
try:
    islip_mwd_body = "Islip Swell Direction: %s " % (islip_mwd) + "\n" + "\n"
except:
    islip_mwd_body = "Islip Swell Direction: %s " % (islip_mwd) + "\n" + "\n"

#WIND
#WIND
#WUNDERGROUND API WIND FORECAST
wunder_1 = "%s: %s at %s mph " % (wu_hour1, wu_wdir1, wu_wspd1) + "\n"
wunder_2 = "%s: %s at %s mph " % (wu_hour2, wu_wdir2, wu_wspd2) + "\n"
wunder_3 = "%s: %s at %s mph " % (wu_hour3, wu_wdir3, wu_wspd3) + "\n" + "\n"
#NDBC VARIABLES
try:
    islip_wdir_body = "Islip Wind Direction: %s " % (islip_wdir) + "\n"
except:
    islip_wdir_body = "Islip Wind Direction: %s " % (islip_wdir) + "\n"
try:
    islip_wspd_body = "Islip Wind Speed: %i mph " % (islip_wspd) + "\n" + "\n"
except:
    islip_wspd_body = "Islip Wind Speed: %s " % (islip_wspd) + "\n" + "\n"

#TIDE
#TIDE
#NOAA TIDE VARIABLES
noaa_tide1 = "%s: %s" % (today_daytime0,today_tide_type0) + "\n"
noaa_tide2 = "%s: %s" % (today_daytime1,today_tide_type1) + "\n"
noaa_tide3 = "%s: %s" % (today_daytime2,today_tide_type2) + "\n"
noaa_tide4 = "%s: %s" % (today_daytime3,today_tide_type3) + "\n" + "\n"

#SUN
#SUN
#WUNDERGROUND API SUNRISE/SET (TODAY ONLY)
wu_sunrise = "Rise: %s:%s" % (sunrise_hour, sunrise_min) + "\n"
wu_sunset = "Set: %s:%s" % (sunset_hour, sunset_min) + "\n" + "\n" + "\n"

#WHAT'S HAPPENING LATER?#WHAT'S HAPPENING LATER?#WHAT'S HAPPENING LATER?#WHAT'S HAPPENING LATER?
#WHAT'S HAPPENING LATER?#WHAT'S HAPPENING LATER?#WHAT'S HAPPENING LATER?#WHAT'S HAPPENING LATER?

#REPORTS
#REPORTS
#SURFLINE VARIABLES
surfline_tomorrow = "%s: %s, %s. %s" % (tomorrow, tomorrow_qual, tomorrow_quant, tomorrow_words) + "\n" + "\n"
surfline_day_after = "%s: %s, %s. %s" % (day_after, day_after_qual, day_after_quant, day_after_words) + "\n" + "\n"

#SWELLINFO VARIABLES
swellinfo_tomorrow = "%s: Swell: %s, Swell Direction: %s, Wind: %s" % (next_6am_time, next_6am_swell, next_6am_swelldirection, next_6am_wind) + "\n" + "\n"
swellinfo_day_after = "%s: Swell: %s, Swell Direction: %s, Wind: %s" % (next2_6am_time, next2_6am_swell, next2_6am_swelldirection, next2_6am_wind) + "\n" + "\n"

#WIND
#WIND
#WUNDERGROUND API WIND FORECAST
wunder_4 = "%s: %s at %s mph " % (wu_hour4, wu_wdir4, wu_wspd4) + "\n"
wunder_5 = "%s: %s at %s mph " % (wu_hour5, wu_wdir5, wu_wspd5) + "\n"
wunder_6 = "%s: %s at %s mph " % (wu_hour6, wu_wdir6, wu_wspd6) + "\n"
wunder_7 = "%s: %s at %s mph " % (wu_hour7, wu_wdir7, wu_wspd7) + "\n"
wunder_8 = "%s: %s at %s mph " % (wu_hour8, wu_wdir8, wu_wspd8) + "\n"
wunder_9 = "%s: %s at %s mph " % (wu_hour9, wu_wdir9, wu_wspd9) + "\n" + "\n"

#TIDE
#TIDE
#NOAA TIDE VARIABLES
noaa_tide5 = "%s: %s" % (tom_daytime0,tom_tide_type0) + "\n"
noaa_tide6 = "%s: %s" % (tom_daytime1,tom_tide_type1) + "\n"
noaa_tide7 = "%s: %s" % (tom_daytime2,tom_tide_type2) + "\n"
noaa_tide8 = "%s: %s" % (tom_daytime0,tom_tide_type3) + "\n" + "\n"
noaa_tide9 = "%s: %s" % (dayafter_daytime0,dayafter_tide_type0) + "\n"
noaa_tide10 = "%s: %s" % (dayafter_daytime1,dayafter_tide_type1) + "\n"
noaa_tide11 = "%s: %s" % (dayafter_daytime2,dayafter_tide_type2) + "\n"
noaa_tide12 = "%s: %s" % (dayafter_daytime3,dayafter_tide_type3) + "\n" + "\n"
#CREATING THE EMAIL VARIABLES /


#/ SENDING THE EMAIL
# TO = "RECIPIENT EMAIL" replace "RECIPIENT EMAIL" with desired email to receive the forecast
SUBJECT = "Today's forecast"
TEXT = main_header + now + reports + surfline + surfline_today + swellinfo + swellinfo_today1 + swellinfo_today2 + swellinfo_today3 + swellinfo_today4 + swellinfo_today5 + swell + ndbc_swell_header + mtk_wvht_body + mtk_dpd_body + mtk_mwd_body + islip_wvht_body + islip_dpd_body + islip_mwd_body + wind + wunderground + wunder_1 + wunder_2 + wunder_3+ ndbc_wind_header + islip_wdir_body + islip_wspd_body + tide + noaa + noaa_tide1 + noaa_tide2 + noaa_tide3 + noaa_tide4 + light + sun + wu_sunrise + wu_sunset + later + reports + surfline_swell_combined + surfline_tomorrow + swellinfo_tomorrow + surfline_day_after + swellinfo_day_after + wind + wunderground + wunder_4 + wunder_5 + wunder_6 + wunder_7 + wunder_8 + wunder_9 + tide + noaa + noaa_tide5 + noaa_tide6 + noaa_tide7 + noaa_tide8 + noaa_tide9 + noaa_tide10 + noaa_tide11 + noaa_tide12

#GMAIL CREDENTIALS
#gmail_sender = "SENDER EMAIL" replace "SENDER EMAIL" with email address for sending email account
#gmail_passwd = "SENDER PW" replace "SENDER PW" with password for sending email account

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_sender, gmail_passwd)

BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

try:
    server.sendmail(gmail_sender, [TO], BODY)
    print("100%% pure adrenaline! Kookcast sent!")
except:
    print("Error sending Kookcast. Life sure has a sick sense of humor, doesn't it?")
server.quit()
#SENDING THE EMAIL /


# / DELETE THE FILES AFTER SENDING EMAIL
try:
    delete_ndbc_files() #the program knows only to read 44025.txt, so multiple versions on HDD result in newest data being named 44025 (1).txt, which the program doesn't recognize as being the file it needs to read
    print()
    print("NDBC files successfully deleted")
except:
    print()
    print("Error deleting NDBC files")
#DELETE THE FILES AFTER SENDING EMAIL /
