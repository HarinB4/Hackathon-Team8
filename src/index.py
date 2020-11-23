import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from src.app import app, COLOR

# Connect to your app pages
from src.apps import app1, app2

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'backgroundColor': COLOR[0]['blue'],
    'color': COLOR[0]['gold']
}

tab_selected_style = {
    'backgroundColor': COLOR[0]['gold'],
    'color': COLOR[0]['blue']
}

# The main app layout
app.layout = html.Div([
    html.Center(
        html.H1('Funded by the UNCG Green Fund')
    ),
    dcc.Location(id='url', refresh=False),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(style=tab_style, selected_style=tab_selected_style, label='Real-Time Interactive Plot', value='tab-1',
                children=[
                ]),
        dcc.Tab(style=tab_style, selected_style=tab_selected_style, id='tab1', label='Average Prediction',
                value='tab-2',
                children=[
                ])
    ], colors={
        "primary": "#0f2044", }
             ),
    html.Br(),

    html.Div(id='page-content', children=[])
])


# This callback is checking which tab the user is on and based on that it will display the desirable tab
@app.callback(Output('page-content', 'children'),
              Input('tabs', 'value'))
def display_page(tab):
    if tab == 'tab-1':
        return app1.layout
    if tab == 'tab-2':
        return app2.layout
    else:
        return "404 Page Error! Please choose a tab"


if __name__ == '__main__':
    app.run_server(debug=False)
