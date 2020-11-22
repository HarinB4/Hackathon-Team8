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

loader = DataLoader.DataLoader()
loop = asyncio.get_event_loop()
loop.run_until_complete(loader.start())

COLOR = ['rgb(31, 119, 180)']

app = dash.Dash(__name__)

entries = os.listdir('../data/Analysis/')
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/Analysis/" + entries[0], parse_dates=['Datetime'],
                 date_parser=lambda col: pd.to_datetime(col, utc=True), index_col='Datetime')
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(children=[

    # The page title
    html.H1("UNCG - Energy consumption", style={'text-align': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Real-Time Interactive Plot', children=[

            # This dropdown is going to loop through the data files, display the names and allow the user to select the meter
            html.Button("Add Filter", id="add-filter", n_clicks=0),
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
        ]),
        dcc.Tab(label='Average Prediction', children=[

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
                id='uncg_graph2'),
        ])]),
],
    style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'})


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
        line=dict(color=COLOR[0]),
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


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
