import asyncio
import os

import dash
from src.models import DataLoader
from threading import Thread

external_stylesheets = ['assets/bWLwgP.css']

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

loader = DataLoader.DataLoader()
# loading thread will stop when main program stops
loader.daemon = True
# start loading data in background
loader.start()


# This variable will take the files name and save them as a list.
entries = loader.get_labels()

COLOR = [{'blue': '#0f2044', 'gold': '#ffb71b'},
         {'gray': '#bec0c2', 'light_blue': '#00698c'},
         {'red': '#a00c30', 'green': '#92d1b3'}]
COLORS = [['#0f2044', '#ffb71b'],
          ['#bec0c2', '#00698c'],
          ['#a00c30', '#92d1b3']]

server = app.server

