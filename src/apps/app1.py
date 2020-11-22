import os
from datetime import datetime

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.models import DataLoader
import asyncio
from src.app import app

loader = DataLoader.DataLoader()
loop = asyncio.get_event_loop()
loop.run_until_complete(loader.start())

entries = os.listdir('../data/Analysis/')
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/Analysis/" + entries[0], parse_dates=['Datetime'],
                 date_parser=lambda col: pd.to_datetime(col, utc=True), index_col='Datetime')

layout = html.Div([
    # This dropdown is going to loop through the data files, display the names and allow the user to select the meter
    html.Button("Select a meter", id="add-filter", n_clicks=0),
    html.Div(id='dropdown-container', children=[]),
    dcc.Checklist(
        id='slct_predict',
        options=[
            {'label': 'Include prediction', 'value': 'Include prediction'},
            {'label': 'Include CI', 'value': 'Include CI'}
        ],
        value=[]
    ),

    dcc.RadioItems(id="slct_period",
                   options=[
                       {'label': 'Hours', 'value': 'H'},
                       {'label': 'Day', 'value': 'D'},
                       {'label': 'Week', 'value': 'W'},
                       {'label': 'Month', 'value': 'M'}
                   ],
                   value='H'
                   ),
    dcc.RadioItems(id="slct_consum",
                   options=[
                       {'label': 'Hourly Energy consumption', 'value': 'Hourly consumption'},
                       {'label': 'Total consumption', 'value': 'Total consumption'},
                       {'label': 'Average Hourly consumption', 'value': 'Average consumption'}
                   ],
                   value='Hourly consumption'
                   ),

    dcc.Graph(
        id='uncg_graph'),
    dcc.RangeSlider(
        id='time_range',
        min=df.index.year.min(),
        max=df.index.year.max(),
        marks={
            i: f'{i}' for i in range(df.index.year.min(), df.index.year.max() + 1, 1)
        },
        value=[df.index.year.min(), df.index.year.max()]
    )
])



@app.callback(
    Output(component_id='uncg_graph', component_property='figure'),

    Output(component_id='time_range', component_property='min'),
    Output(component_id='time_range', component_property='max'),
    Output(component_id='time_range', component_property='marks'),
    Output(component_id='time_range', component_property='value'),

    [Input(component_id='slct_predict', component_property='value')],
    [Input(component_id='slct_period', component_property='value')],
    [Input(component_id='slct_consum', component_property='value')],
    Input({'type': 'slct_meter', 'index': ALL}, 'value'),
    [State(component_id='time_range', component_property='value')]

)
def update_graph(slct_predict, slct_period, slct_consum, slct_meter, time_range):
    df = {}
    for i in range(len(slct_meter)):
        df[i] = loader.load_file(slct_meter[i])
    # print(df[0])

    start_time = df[0][df[0].index.year == time_range[0]]
    start_time = start_time.index.min()

    end_time = df[0][df[0].index.year == time_range[1]]
    end_time = end_time.index.max()

    if (type(start_time) == pd._libs.tslibs.nattype.NaTType):
        start_time = df[0].index.min()
    print(start_time)
    print(end_time)

    fig = go.Figure()
    for i in range(len(df)):
        if slct_consum == 'Total consumption':
            dff = df[i].loc[start_time:end_time].resample(slct_period).sum()
        elif slct_consum == 'Average consumption':
            dff = df[i].loc[start_time:end_time].resample(slct_period).mean()
        # temp
        elif slct_consum == 'Hourly consumption':
            dff = df[i].loc[start_time:end_time]

        # Add traces
        fig.add_trace(go.Scatter(
            name='Actual ' + slct_meter[i],
            x=dff.index,
            y=dff['Actual'],
            mode='lines',
            # line=dict(color=COLOR[0]),
        ))
        # print(slct_predict)
        # print(len(slct_predict))
        if ('Include prediction' in slct_predict):
            fig.add_trace(go.Scatter(x=dff.index, y=dff['Predicted'],
                                     mode='lines',
                                     name='Predicted ' + slct_meter[i]))
        if ('Include CI' in slct_predict):
            fig.add_traces([
                go.Scatter(
                    name='Upper Bound',
                    x=dff.index,
                    y=dff['obs_ci_upper'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                ),
                go.Scatter(
                    name='Lower Bound',
                    x=dff.index,
                    y=dff['obs_ci_lower'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(68, 68, 68, 0.3)',
                    fill='tonexty',
                    showlegend=False
                )
            ])

        # fig = px.line(x=dff.index, y=dff['Actual'])

        fig.update_layout(
            hovermode="x",
            yaxis=dict(
                title_text=slct_consum,
            ),
            xaxis=dict(
                title_text='Time',
            )
        )
    min, max, marks, value = loader.x(slct_meter[i])

    return fig, min, max, marks, value


@app.callback(
    Output('dropdown-container', 'children'),
    Input('add-filter', 'n_clicks'),
    State('dropdown-container', 'children'))
def display_dropdowns(n_clicks, children):
    print(n_clicks)
    if n_clicks < 3:
        new_dropdown = dcc.Dropdown(
            id={
                'type': "slct_meter",
                'index': n_clicks
            },
            options=[{'label': i.split('_results.csv')[0], 'value': i.split('_results.csv')[0]} for i in entries],
            value='BryanDataCenter',
            style={'display': 'inline-block',
                   'width': '300px'}
        )
        children.append(new_dropdown)
        return children
    return children