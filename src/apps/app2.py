import os
from datetime import datetime

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL

import pandas as pd
import plotly.graph_objects as go
from src.app import app


entries = os.listdir('../data/Analysis/')
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/Analysis/" + entries[0], parse_dates=['Datetime'],
                 date_parser=lambda col: pd.to_datetime(col, utc=True), index_col='Datetime')

layout = html.Div([
    # This dropdown is going to loop through the data files, display the names and allow the user to select the meter
    dcc.Dropdown(id="slct_meter2",
                 options=[{'label': i.split('_results')[0], 'value': i} for i in entries],
                 multi=False,
                 value=entries[0],
                 style={'width': "40%"}
                 ),

    dcc.RadioItems(id="slct_period2",
                   options=[
                       {'label': 'Month', 'value': 'MS'},
                       {'label': 'Week of year', 'value': 'W'},
                       {'label': 'Day of week', 'value': 'D'},
                       {'label': 'Hour of day', 'value': 'H'}

                   ],
                   value='MS'
                   ),
    dcc.Graph(
        id='uncg_graph2')
])


@app.callback(
    Output(component_id='uncg_graph2', component_property='figure'),
    [Input(component_id='slct_meter2', component_property='value')],
    [Input(component_id='slct_period2', component_property='value')],

)
def update_graph2(slct_meter2, slct_period2):
    df1 = pd.read_csv("../data/Analysis/" + slct_meter2, parse_dates=['Datetime'],
                      date_parser=lambda col: pd.to_datetime(col, utc=True), index_col='Datetime')

    start_time = df1[df1.index.year == 2020]
    start_time = start_time.index.min()

    dff1 = df1.loc[start_time:].resample(slct_period2).mean()
    time = 'Months'
    list = ['Jan', 'Feb', "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

    if slct_period2 == 'W':
        dff1 = df1.loc[start_time:].resample(slct_period2).mean()
        dff1.index = dff1.index.isocalendar().week
        dff1 = dff1.groupby(level=0).mean()
        list = dff1.index
        time = 'Weeks'


    elif slct_period2 == 'D':
        dff1 = df1.loc[start_time:].resample(slct_period2).mean()
        dff1.index = dff1.index.dayofweek
        dff1 = dff1.groupby(level=0).mean()
        list = ['Monday', 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        time = 'Days'


    elif slct_period2 == 'H':
        dff1 = df1.loc[start_time:].resample(slct_period2).mean()
        dff1.index = dff1.index.hour
        dff1 = dff1.groupby(level=0).mean()
        list = ['12:00 am', '1:00 am', '2:00 am', '3:00 am', '4:00 am', '5:00 am', '6:00 am', '7:00 am',
                '8:00 am', '9:00 am', '10:00 am', '11:00 am', '12:00 pm', '1:00 pm', '2:00 pm', '3:00 pm', '4:00 pm',
                '5:00 pm', '6:00 pm', '7:00 pm', '8:00 pm', '9:00 pm', '10:00 pm', '11:00 pm', '12:00 pm', ]
        time = 'Hours'

    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(
        name='Actual',
        x=list,
        y=dff1['Actual'],
        mode='markers',
    ))

    fig.add_trace(go.Scatter(x=list, y=dff1['Predicted'],
                             mode='lines',
                             name='Predicted'))

    # fig = px.line(x=dff.index, y=dff['Actual'])

    fig.update_layout(
        hovermode="x",
        yaxis=dict(
            title_text='Average Consumption',
        ),
        xaxis=dict(
            title_text=time,
        )
    )

    return fig
