import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/Analysis/Baseball_results.csv")

df['Datetime'] = pd.to_datetime(df["Datetime"])

print(df)
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("UNCG - Energy consumption", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_meter",
                 options=[
                     {"label": "Baseball", "value": 'Baseball_results'},
                     {"label": "BaseballFieldSupportBldg_results", "value": 'BaseballFieldSupportBldg_results'},
                     {"label": "BaseballStadiumPrkLights_results", "value": 'BaseballStadiumPrkLights_results'}],
                 multi=False,
                 value='Baseball_results',
                 style={'width': "40%"}
                 ),
    dcc.RadioItems(id="slct_period",
                   options=[
                       {'label': 'Hours', 'value': 'Hours'},
                       {'label': 'Day', 'value': 'Day'},
                       {'label': 'Week', 'value': 'Week'},
                       {'label': 'Month', 'value': 'Month'}
                   ],
                   value='Hours'
                   ),
    dcc.RadioItems(id="slct_consum",
                   options=[
                       {'label': 'Hourly consumption', 'value': 'hr_consumption'},
                       {'label': 'Total consumption', 'value': 'tot_consumption'},
                       {'label': 'Average consumption', 'value': 'avr_consumption'}
                   ],
                   value='hr_consumption'
                   ),
    html.Div(id='output_container', children=[]),
    html.Br(),

    # dcc.Graph(id='uncg_graph', figure={})
    dcc.Graph(
        id='uncg_graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
            ],
            'layout': {
                'title': '2015 hours meter museum'
            }
        }
    )

])


# @app.callback(
#     [Output(component_id='uncg_graph', component_property='figure')],
#
#     [Input(component_id='slct_meter', component_property='value')],
#     [Input(component_id='slct_period', component_property='value')],
#     [Input(component_id='slct_consum', component_property='value')],
# )
# def update_graph(slct_meter, slct_period, slct_consum):
#     pass


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
