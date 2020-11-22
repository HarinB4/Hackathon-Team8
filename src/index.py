import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from src.app import app

# Connect to your app pages
from src.apps import app1, app2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Real-Time Interactive Plot', value='tab-1', children=[
        ]),
        dcc.Tab(id='tab1', label='Average Prediction', value='tab-2', children=[
        ])
    ])
    ,
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              Input('tabs', 'value'))
def display_page(tab):
    if tab == 'tab-1':
        return app1.layout
    if tab == 'tab-2':
        return app2.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
