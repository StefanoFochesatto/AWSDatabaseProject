## Data IO\Manipulation libraries
import pandas as pd
import numpy as np
from sqlalchemy import  create_engine

## Dashboard Libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from os import environ

AWSKEY = str(environ.get('AWSENGINE'))
AZUREKEY = str(environ.get('AZUREENGINE'))
GCPKEY = str(environ.get('GCPENGINE'))


## CSS Style Sheet for Dash Components
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

## Init Dash App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

## Make connection to MySQL database, AWS by default
engine = create_engine(AWSKEY)

## dash app layout
app.layout = html.Div([
     ## Database dropdown menu
     html.Div(
                [
                    html.H6("""Select Database Backend""",
                            style={'margin-right': '2em'})
                ],
            ),

        dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Amazon Web Services', 'value': 'AWS'},
            {'label': 'Microsoft Azure', 'value': 'AZR'}, 
            {'label': 'Google Cloud Platform', 'value': 'GCP'}
        ],
        value='AWS'
    ), 
        ## Graph
        dcc.Graph(
            id='map_with_slider', 
            style={'width': '100vw', 'height': '80vh', 'textAlign': 'left', 'font-weight':'300'}
            ),

    ## Year Slider
        dcc.Slider(
            id='year_slider',
            min = 1992, 
            max = 2015,
            value = 1992, 
            step = 1,   
            marks = {year: str(year) for year in range(1992,2016)}
        ), 
     dcc.Store(id='intermediate-value')
    ])

## Callback for Database menu
@app.callback(Output('intermediate-value', 'data'),[Input("demo-dropdown", "value")] )
def change_backend(value):
    # reference global engine object
    global engine 
    # if statement to change databases
    if (value == 'AWS'):
        engine =  create_engine(AWSKEY)
    elif (value == 'AZR'):
        engine =  create_engine(AZUREKEY)
    elif (value == 'GCP'):
        engine =  create_engine(GCPKEY)
    
    return 1



## Callback for Year slider
@app.callback(
    Output("map_with_slider", "figure"), 
    Input("intermediate-value", "data"),
    Input("year_slider", "value"))
def display_map(extra, year):
        query = 'select FIRE_YEAR,LATITUDE,LONGITUDE from Fires use index(FireYearIndex) where FIRE_YEAR = {} ORDER BY RAND() limit 500'.format(year)
        with engine.connect() as connection:
          result_dataFrame = pd.read_sql(query, connection)
        
        
        data = [
            go.Scattergeo(
                lat = result_dataFrame['LATITUDE'], 
                lon = result_dataFrame['LONGITUDE']
            )
        ]

        layout = go.Layout(
          title = dict(
            text= '500 Random Fires During {}'.format(year),
            font=dict(
                family="Helvetica Neue",
                size=20,
                color='#000000'
                )
            ),

          margin = dict(
              autoexpand=True,
                l=0, #left margin
                r=0, #right margin
                b=0, #bottom margin
                t=50  #top margin
          ),

          geo = dict(
            scope='usa', 
            landcolor='aliceblue', 
            projection=dict(type='albers usa'), 
            showland = True, 
          )
        )

        return {'data':data, 'layout':layout}


if __name__ == '__main__':
    app.run_server(debug=True)

