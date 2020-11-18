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

df


df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("UNCG - Energy conception", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_meter",
                 options=[
                     {"label": "Baseball", "value": 'Baseball_results'},
                     {"label": "BaseballFieldSupportBldg_results", "value": 'BaseballFieldSupportBldg_results'},
                     {"label": "BaseballStadiumPrkLights_results", "value": 'BaseballStadiumPrkLights_results'}],
                 multi=False,
                 value='Baseball_results',
                 style={'width': "40%"}
                 ),
    dcc.RadioItems(
        options=[
            {'label': 'Hours', 'value': 'Hours'},
            {'label': 'Day', 'value': 'Day'},
            {'label': 'Week', 'value': 'Week'},
            {'label': 'Month', 'value': 'Month'}
        ],
        value='Hours'
    ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    # dcc.Graph(id='my_bee_map', figure={})
    dcc.Graph(
            id='uncg_graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': '2015 hours meter museum'
                }
            }
        )

])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='uncg_graph', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Datetime"].split(' ')[0].split('-')[0] == option_slctd]
    dff = dff[dff["Actual"] == "Varroa_mites"]
    print(dff)
    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        # locationmode='USA-states',
        # locations='state_code',
        # scope="usa",
        # color='Pct of Colonies Impacted',
        # hover_data=['State', 'Pct of Colonies Impacted'],
        # color_continuous_scale=px.colors.sequential.YlOrRd,
        # labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        # template='plotly_dark'
    )


    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
