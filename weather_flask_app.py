# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 01:37:36 2024

@author: ML
"""

from flask import Flask, render_template, session
import webbrowser as wb

import pandas as pd

import plotly.express as px
import plotly

import plotly.graph_objects as go
import plotly.tools as tls

import json

from datetime import datetime as dt
from datetime import timedelta

from weather_data import get_weather_data, get_weather_data_list, datetime_to_string

def days_ago(ago=1, para="temperature1havg"):
    print(ago)
    
    endtime = dt.now()
    end = datetime_to_string(endtime)
    startime = dt.now()-timedelta(days=max(1,ago))
    start = datetime_to_string(startime)
    
    df = get_weather_data_list(start, end, ["kumpula","lohja", "espoo", "vantaa"], parame=para) 
    return df

def row(a, b):
    return "{} : {}".format(a, b)

def get_fig_5(days=2, station_name="kumpula"):
    global df
    df = days_ago(days)
    fig = px.line(df[df.station==station_name], x="time", y="value", title='Temperature')
    
    return fig
     
app = Flask(__name__)

@app.route('/')
def home():
   global fig
   fig = get_fig_5()
   # Create graphJSON
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
   # Use render_template to pass graphJSON to html
   return render_template('plotti4.html', graphJSON=graphJSON)

@app.route('/weather')
def weather():
   fig = get_fig_5()
   
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   #return render_template('index.html')
   return render_template('plotti4.html', graphJSON=graphJSON)
   
url = "http://127.0.0.1:5000/weather"

wb.open(url)

if __name__ == '__main__':
   app.run()