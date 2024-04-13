# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 22:37:47 2024

@author: ML
"""

import os
import contextlib

import pandas as pd
import numpy as np

import subprocess 

import requests

import xmltodict
from xml.dom.minidom import parse, parseString

from datetime import datetime as dt
from datetime import timedelta 

@contextlib.contextmanager
def visit_dir(dirname):
    curdir = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(curdir)
        
class Fish:
    def __init__(self, data):
        self.data=data
        
def get_request(url):
    r = requests.get(url)
    return r

def zero_string(num, n=2):
    s = str(num)
    return "0"*(max(0,n-len(s)))+s

def datestring(hour, day, month, year=2023):
    fhour = zero_string(hour)
    fday = zero_string(day)
    fmonth = zero_string(month)
    
    time = "{}-{}-{}T{}:00:00Z".format(year, fmonth, fday, fhour)
    
    return time

def datetime_to_string(dat):
    h,d,m,y = dat.hour,dat.day,dat.month,dat.year
    return datestring(h,d,m,y)
    
APIKEY = ""

def test_1():
    starttime = "2023-06-06T00:00:00Z"
    #starttime = "2024-01-01T00:00:00Z"
    stoptime = "2023-06-07T00:00:00Z"
    
    starttime = "2023-06-01T00:00:00Z"
    #starttime = "2024-01-01T00:00:00Z"
    endtime = "2023-06-30T00:00:00Z"
    
    starttime = datestring(0,1,1)
    endtime = datestring(0,2,1)
    
    query = "fmi::observations::weather::hourly::simple"
    #query = "fmi::radar::composite::rr"
    
    place = "helsinki"
    place = "lohja"
    place = "kumpula"
    
    #url = f"https://opendata.fmi.fi/wfs?request=getFeature&storedquery_id=fmi::observations::weather::hourly::simple&place={place}&starttime={starttime}"
    #url = f"https://opendata.fmi.fi/wfs?request=getFeature&storedquery_id=fmi::observations::weather::hourly::simple&place={place}&starttime={starttime}&stoptime={stoptime}"
    
    url = f"https://opendata.fmi.fi/wfs?request=getFeature&storedquery_id={query}&place={place}&starttime={starttime}&endtime={endtime}"
    #url = f"https://opendata.fmi.fi/wfs?request=getFeature&storedquery_id={query}&lon={lon}&lat={lat}&starttime={starttime}&endtime={endtime}"
    
    r = get_request(url).text
    
    p = parseString(r)
    
    pdict = xmltodict.parse(r)
    
    datamain = pdict["wfs:FeatureCollection"]["wfs:member"]
    
    header = pdict["wfs:FeatureCollection"]
    
    paras = [
        'TA_PT1H_AVG',
        'TA_PT1H_MAX',
        'TA_PT1H_MIN',
        'RH_PT1H_AVG',
        'WS_PT1H_AVG',
        'WS_PT1H_MAX',
        'WS_PT1H_MIN',
        'WD_PT1H_AVG',
        'PRA_PT1H_ACC,'
        'PRI_PT1H_MAX',
        'PA_PT1H_AVG',
        'WAWA_PT1H_RANK' 
    ]
    
    para = "PRA_PT1H_ACC"
    para = "PRA_PT1H_ACC"
    
    data_dict = {}
    
    for mem in datamain:
        entry = mem['BsWfs:BsWfsElement']
        
        paraname = entry['BsWfs:ParameterName']
        value = entry['BsWfs:ParameterValue']
        time = entry['BsWfs:Time']
        if not time in data_dict:
            data_dict[time] = {}
            
        data_dict[time][paraname] = float(value)
        
        if paraname == para:
            print(time, paraname, value)
    
    table = pd.DataFrame(data_dict).transpose()
    rain = table["PRA_PT1H_ACC"]
    
def test_2():
    test_1()
        
    endtime = dt.now()
    end = datetime_to_string(endtime)
    startime = dt.now()-timedelta(days=1)
    start = datetime_to_string(startime)
    
    print("")
    
    for t,p,v in get_weather_data(start,end,"kumpula"):
        print(t,p,v)
        
    endtime = dt.now()
    end = datetime_to_string(endtime)
    startime = dt.now()-timedelta(days=1)
    start = datetime_to_string(startime)
    
    l = get_weather_data_list(start, end, ["kumpula","lohja"], parametre="sade1hacc") 
    
def get_weather_data(starttime, endtime, station, parametre="sade1hacc"):
    
    global r
    global data_dict
    global para
    
    #urlin väsäys
    
    query = "fmi::observations::weather::hourly::simple"
    url = f"https://opendata.fmi.fi/wfs?request=getFeature&storedquery_id={query}&place={station}&starttime={starttime}&endtime={endtime}"
    
    #url get
    
    r = get_request(url).text
    p = parseString(r)
    
    _paras = {
        'temperature1havg':'TA_PT1H_AVG',
        'temperature1hmax':'TA_PT1H_MAX',
        'temperature1hmin':'TA_PT1H_MIN',
        'rhumid1hmin':'RH_PT1H_AVG',
        'snow1havg':'WS_PT1H_AVG',
        'snow1hmax':'WS_PT1H_MAX',
        'snow1hmin':'WS_PT1H_MIN',
        'wd1hacc' :'WD_PT1H_AVG',
        'sade1hacc':'PRA_PT1H_ACC',
        'sade1hmax':'PRI_PT1H_MAX',
        'paine1havg':'PA_PT1H_AVG',
        'ww1hmin':'WAWA_PT1H_RANK' 
    }
    
    paras = {
        'TEMPERATURE_1H_AVG':'TA_PT1H_AVG',
        'TEMPERATURE_1H_MAX':'TA_PT1H_MAX',
        'TEMPERATURE_1H_MIN':'TA_PT1H_MIN',
        'HUMIDITY_1H_AVG':'RH_PT1H_AVG',
        'SNOW_1H_AVG':'WS_PT1H_AVG',
        'SNOW_1H_MAX':'WS_PT1H_MAX',
        'SNOW_1H_MIN':'WS_PT1H_MIN',
        'WIND_1H_AVG' :'WD_PT1H_AVG',
        'RAIN_1H_ACC':'PRA_PT1H_ACC',
        'RAIN_1H_MAX':'PRI_PT1H_MAX',
        'ATMOPRESSURE_1H_AVG':'PA_PT1H_AVG',
        'WIND_1H':'WAWA_PT1H_RANK' 
    }
    
    #parserointi, parsee
    
    para = paras[parametre]
    
    pdict = xmltodict.parse(r)
    datamain = pdict["wfs:FeatureCollection"]["wfs:member"]
    header = pdict["wfs:FeatureCollection"]
    
    data_dict = {}
    
    for mem in datamain:
        entry = mem['BsWfs:BsWfsElement']
        
        paraname = entry['BsWfs:ParameterName']
        value = entry['BsWfs:ParameterValue']
        time = entry['BsWfs:Time']
        if not time in data_dict:
            data_dict[time] = {}
            
        data_dict[time][paraname] = float(value)
        
        if paraname == para:
            yield time, paraname, value, station
    
    
def get_weather_data_list(starttime, endtime, stations, parame="sade1hacc"):
    
    ll = []
    for station in stations:
        l = list(get_weather_data(starttime, endtime, station, parametre=parame))
        ll = ll+l
        
    data = pd.DataFrame(ll)
    
    data.columns = ["time","parametre","value","station"]

    data.value = pd.to_numeric(data.value, downcast='float', errors="coerce")
    
    return data

    
    