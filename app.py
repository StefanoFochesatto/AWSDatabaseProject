import pandas as pd
import numpy as np
from sqlalchemy import  create_engine



import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


engine = create_engine("mysql+mysqlconnector://gsfochesatto:Stef129763@awsdatabase.c21iv83neop4.us-east-2.rds.amazonaws.com/FireData")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
        dcc.Graph(
            id='map_with_slider', 
            style={'width': '100vw', 'height': '90vh', 'textAlign': 'center'}
            ), 

        dcc.Slider(
            id='year_slider',
            min = 1992, 
            max = 2015,
            value = 1992, 
            step = 1,   
            marks = {year: str(year) for year in range(1992,2016)}
        )
    ])



@app.callback(
    Output("map_with_slider", "figure"), 
    [Input("year_slider", "value")])
def display_map(year):
        query = 'select FIRE_YEAR,LATITUDE,LONGITUDE from Fires where FIRE_YEAR = {} ORDER BY RAND() limit 500'.format(year)
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
            projection=dict(type='albers usa'), 
            showland = True, 
          )
        )
        return {'data':data, 'layout':layout}

if __name__ == '__main__':
    app.run_server()

