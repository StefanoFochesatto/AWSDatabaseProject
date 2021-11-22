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

## CSS Style Sheet for Dash Components
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

## Init Dash App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

## Make connection to MySQL database, AWS by default
engine = create_engine("mysql+mysqlconnector://gsfochesatto:Stef129763@awsdatabase.c21iv83neop4.us-east-2.rds.amazonaws.com/FireData")

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
            style={'width': '100vw', 'height': '80vh', 'textAlign': 'center'}
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
        engine =  create_engine("mysql+mysqlconnector://gsfochesatto:Stef129763@awsdatabase.c21iv83neop4.us-east-2.rds.amazonaws.com/FireData")
    elif (value == 'AZR'):
        engine =  create_engine("mysql+mysqlconnector://gsfochesatto@azuredatabasecloudlab:Stef129763@azuredatabasecloudlab.mysql.database.azure.com/FireData")
    elif (value == 'GCP'):
        engine =  create_engine("mysql+mysqlconnector://root:Stef129763@34.72.83.33/FireData")
    
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
          title = '500 Random Fires in the U.S in {}'.format(str(year)), 
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

