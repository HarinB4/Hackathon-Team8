import dash_core_components as dcc
import dash_html_components as html
from dash import dash
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
import plotly.graph_objects as go
from src.app import app, loader, entries, COLORS

df = loader.load_file(entries['Name'][0])

# Create app1 layout
layout = html.Div([
    # This dropdown is going to loop through the data files, display the names and allow the user to select the meter
    html.Button("Add a meter", id="add-filter", n_clicks=0),
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
                       {'label': 'Hours', 'value': 'H', 'disabled': False},
                       {'label': 'Day', 'value': 'D', 'disabled': True},
                       {'label': 'Week', 'value': 'W', 'disabled': True},
                       {'label': 'Month', 'value': 'M', 'disabled': True}
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
    dcc.Loading(
        id="loading-2",
        children=[
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
        ],
        type="circle",
    ),
])


# This callback method is taking the necessary input to plot the desirable graph
@app.callback(
    Output(component_id='uncg_graph', component_property='figure'),
    Output(component_id='time_range', component_property='min'),
    Output(component_id='time_range', component_property='max'),
    Output(component_id='time_range', component_property='marks'),
    Output(component_id='slct_period', component_property='options'),

    [Input(component_id='slct_predict', component_property='value')],
    [Input(component_id='slct_period', component_property='value')],
    [Input(component_id='slct_consum', component_property='value')],
    Input({'type': 'slct_meter', 'index': ALL}, 'value'),
    [Input(component_id='time_range', component_property='value')],

)
def update_graph(slct_predict, slct_period, slct_consum, slct_meter, time_range):
    # in case there is the user didn't select a meter exit the function
    if len(slct_meter) == 0:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # create a dataframe dictionary that hold all the user choice
    dfs = {}
    for i in range(len(slct_meter)):
        dfs[i] = loader.load_file(slct_meter[i])

    # Take the first meter selected by the user and
    # set the time range of the graph based on that.
    start_time = dfs[0][dfs[0].index.year == time_range[0]].index.min()
    end_time = dfs[0][dfs[0].index.year == time_range[1]].index.max()

    # This statement will handle the case where the first meter doesn't contain the minimal year.
    if type(start_time) == pd._libs.tslibs.nattype.NaTType:
        start_time = dfs[0].index.min()

    # This will create graph object based on the user filters selection
    fig = go.Figure()
    for i in range(len(dfs)):
        if slct_consum == 'Total consumption':
            dff = dfs[i].loc[start_time:end_time].resample(slct_period).sum()
        elif slct_consum == 'Average consumption':
            dff = dfs[i].loc[start_time:end_time].resample(slct_period).mean()
        # temp
        elif slct_consum == 'Hourly consumption':
            dff = dfs[i].loc[start_time:end_time]

        # Add traces
        fig.add_trace(go.Scatter(
            name='Actual ' + slct_meter[i],
            x=dff.index,
            y=dff['Actual'],
            mode='lines',
            marker_color=COLORS[i][0]
        ))
        # This will add the prediction trace to the graph object when the user select prediction option.
        if 'Include prediction' in slct_predict:
            fig.add_trace(go.Scatter(x=dff.index, y=dff['Predicted'],
                                     mode='lines',
                                     name='Predicted ' + slct_meter[i],
                                     marker_color=COLORS[i][1])
                          )
        # This will add the confident interval trace to the graph object when the user select confident interval option.
        if 'Include CI' in slct_predict:
            fig.add_traces([
                go.Scatter(
                    name='Upper Bound',
                    x=dff.index,
                    y=dff['obs_ci_upper'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False,
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

        fig.update_layout(
            hovermode="x",
            yaxis=dict(
                title_text=slct_consum,
            ),
            template='plotly_white',
            xaxis=dict(
                title_text='Time',
            )
        )
    if slct_consum == 'Hourly consumption':
        period_option = [
            {'label': 'Hours', 'value': 'H', 'disabled': False},
            {'label': 'Day', 'value': 'D', 'disabled': True},
            {'label': 'Week', 'value': 'W', 'disabled': True},
            {'label': 'Month', 'value': 'M', 'disabled': True}
        ]
    else:
        period_option = [
            {'label': 'Hours', 'value': 'H', 'disabled': True},
            {'label': 'Day', 'value': 'D', 'disabled': False},
            {'label': 'Week', 'value': 'W', 'disabled': False},
            {'label': 'Month', 'value': 'M', 'disabled': False}
        ]

    # This will change the RangeSilder values
    min, max, marks = range_slider_optimizer(slct_meter[0])
    return fig, min, max, marks, period_option


# This helper method will handle the RangeSlider values
def range_slider_optimizer(slct_meter):
    df = loader.load_file(slct_meter)
    min = df.index.year.min()
    max = df.index.year.max()
    marks = {i: f'{i}' for i in range(df.index.year.min(), df.index.year.max() + 1, 1)}
    return min, max, marks


# This callback will handle adding multiple meter dropdowns.
@app.callback(
    Output('dropdown-container', 'children'),
    Input('add-filter', 'n_clicks'),
    State('dropdown-container', 'children'))
def display_dropdowns(n_clicks, children):
    number_of_children = 3

    if n_clicks < number_of_children:
        new_dropdown = dcc.Dropdown(
            id={
                'type': "slct_meter",
                'index': n_clicks
            },
            options=[{'label': entries['Label'][i], 'value': entries['Name'][i]} for i in entries.index],
            value=entries['Name'][0],
            style={'display': 'inline-block',
                   'width': '300px'}
        )
        children.append(new_dropdown)
        return children
    return children
