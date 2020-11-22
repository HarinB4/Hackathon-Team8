import asyncio
import os

import dash
from src.models import DataLoader

app = dash.Dash(__name__, suppress_callback_exceptions=True)

loader = DataLoader.DataLoader()
loop = asyncio.get_event_loop()
loop.run_until_complete(loader.start())

# This variable will take the files name and save them as a list.
entries = list(map(lambda sub: sub.split('_results.csv')[0], os.listdir('../data/Analysis/')))

server = app.server
