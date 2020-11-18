import os

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)

entries = os.listdir('../data/Analysis/')

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/Analysis/Baseball_results.csv")

df['Datetime'] = pd.to_datetime(df["Datetime"])

df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    # The page title
    html.H1("UNCG - Energy consumption", style={'text-align': 'center'}),

    # This dropdown is going to loop through the data files, display the names and allow the user to select the meter
    dcc.Dropdown(id="slct_meter",
                 options=[{'label': i.split('_results')[0], 'value': i} for i in entries],
                 multi=False,
                 value=entries[0],
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
    html.Br(),
    dcc.Graph(
        id='uncg_graph',
        hoverData={'points': [{'customdata': 'Japan'}]}
    )
], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'})

@app.callback(
    [Output(component_id='uncg_graph', component_property='figure')],
    [Input(component_id='slct_meter', component_property='value')],
    [Input(component_id='slct_period', component_property='value')],
    [Input(component_id='slct_consum', component_property='value')],
)
def update_graph(slct_meter, slct_period, slct_consum):
    df = pd.read_csv("../data/Analysis/" + slct_meter)

    df['Datetime'] = pd.to_datetime(df["Datetime"])

    fig = px.scatter(x=df['Datetime'].year,
                y=df['Actual'],
                # hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
                )
    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
