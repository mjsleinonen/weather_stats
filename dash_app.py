# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:59:04 2024

@author: ML
"""

import numpy as np

import webbrowser as wb

import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_daq as daq

import plotly.express as px
import pandas as pd

from datetime import datetime as dt
from datetime import timedelta 

from weather_data import get_weather_data, get_weather_data_list, datetime_to_string

from flask import request

## DATA FUNCTIONS
##############################################################################

endtime = dt.now()
end = datetime_to_string(endtime)
startime = dt.now()-timedelta(days=1)
start = datetime_to_string(startime)

stations = ["kumpula","lohja", "espoo", "vantaa", "vihti"]

df_init = get_weather_data_list(start, end, stations, parame="temperature1havg") 

def get_data_table(start, end, para):
    df = get_weather_data_list(start, end, stations, parame=para)
    return df

def days_ago(ago=1, para="temperature1havg"):
    print(ago)
    
    endtime = dt.now()
    end = datetime_to_string(endtime)
    startime = dt.now()-timedelta(days=max(1,ago))
    start = datetime_to_string(startime)
    
    df = get_weather_data_list(start, end, ["kumpula","lohja", "espoo", "vantaa"], parame=para) 
    
    return df
    
## INIT APP    
##############################################################################
    
app = Dash(__name__)

#STYLES
###############################################################################

sh_1 = {'textAlign': 'left'}

#INITIAL DATA AND PARAMETERS
###############################################################################

kumpula = df_init[df_init.station=="kumpula"].to_dict('records')

paras =  [
        'temperature1havg',
        'temperature1hmax',
        'temperature1hmin',
        'rhumid1hmin',
        'snow1havg',
        'snow1hmax',
        'snow1hmin',
        'wd1hacc',
        'sade1hacc',
        'sade1hmax',
        'paine1havg',
        'ww1hmin'    
]

# APP LAYOUT AND CALLBACKS
###############################################################################

app.layout = html.Div([
    html.H1(children='Sää-Äppi', style={'textAlign':'center'}),
    dcc.Dropdown(stations, 'kumpula', id='dropdown-selection'),
    dcc.Dropdown(paras, 'temperature1havg', id='dropdown-selection2'),
    daq.NumericInput(id='my-numeric-input-1', value=1),
    dcc.Graph(id='graph-content'),
    dash_table.DataTable(id='table', data=kumpula, page_size=10, style_cell=sh_1, style_header=sh_1)
])

@callback(
    Output('table', 'data'),
    [
     Input('dropdown-selection', 'value'),
     Input('dropdown-selection2', 'value')
    ]
    
)
def update_table(station, parameter):
    #df = get_weather_data_list(start, end, [station], parame=parameter)
    dff = df_init[df_init.station==station].to_dict('records')
    return dff

@callback(
    Output('graph-content', 'figure'),
    [
     Input('dropdown-selection', 'value'),
     Input('my-numeric-input-1', 'value'),
     Input('dropdown-selection2','value')
    ]
)
def update_output(value, numvalue, parameter):
    if numvalue==None:
        numago = 2
    else:
        numago = numvalue
    app.logger.info(numago)
    df = days_ago(numago, parameter)
    dff = df[df.station==value]
    plex =  px.line(dff, x='time', y='value')
    return plex

# POP PAGE, RUN APP
###############################################################################

runap = False
runap = True

if __name__ == '__main__' and runap:
    
    url = r"http://127.0.0.1:8050/"
    wb.open(url)
    
    app.run(debug=True, dev_tools_silence_routes_logging = False)
