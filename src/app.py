import asyncio
import os

import dash
from src.models import DataLoader

external_stylesheets = ['assets/bWLwgP.css']

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

loader = DataLoader.DataLoader()
loop = asyncio.get_event_loop()
loop.run_until_complete(loader.start())

# This variable will take the files name and save them as a list.
entries = list(map(lambda sub: sub.split('_results')[0], loader.get_file_names()))

COLOR = [{'blue': '#0f2044', 'gold': '#ffb71b'},
         {'gray': '#bec0c2', 'light_blue': '#00698c'},
         {'red': '#a00c30', 'green': '#92d1b3'}]
COLORS = [['#0f2044', '#ffb71b'],
          ['#bec0c2', '#00698c'],
          ['#a00c30', '#92d1b3']]

server = app.server
