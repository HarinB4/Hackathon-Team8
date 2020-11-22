import os
import pandas as pd
import asyncio
import time


class DataLoader:
    files = None
    data = None
    file_names = None
    DIR = '../data/Analysis/'
    min = None
    max = None
    value = None
    marks = None

    def __init__(self):
        self.files = [file for file in os.listdir(self.DIR) if file.endswith('.csv')]
        # turn filename.csv to filename for all files
        self.file_names = [os.path.splitext(os.path.basename(x))[0] for x in self.files]
        self.file_names
        self.file_names.sort()
        self.data = {}

    async def start(self):
        # start loading all data function and forget about it
        asyncio.ensure_future(self.load_all_data())

    async def load_all_data(self):
        # this function loads all data in the Analysis directory
        await asyncio.sleep(1)
        if self.data == {}:
            for i in range(len(self.file_names)):
                try:
                    self.data[self.file_names[i]] = pd.read_csv(self.DIR + self.files[i], parse_dates=['Datetime'])
                except FileNotFoundError:
                    self.data[self.file_names[i]] = pd.DataFrame()

    def load_file(self, file_name) -> pd.DataFrame:
        # this function loads a single specified file
        try:
            if file_name in self.data:
                if len(self.data[file_name]) != 0:
                    return self.data[file_name]
            else:
                return pd.read_csv(self.DIR + file_name + '_results.csv', parse_dates=['Datetime'],
                                   date_parser=lambda col: pd.to_datetime(col, utc=True), index_col='Datetime')
        except FileNotFoundError:
            return {file_name: pd.DataFrame([])}

    def get_file_names(self):
        # this function returns a list of file names
        return self.file_names

    def x(self, slct_meter):
        df = self.load_file(slct_meter)
        min = df.index.year.min()
        max = df.index.year.max()
        marks = {i: f'{i}' for i in range(df.index.year.min(), df.index.year.max() + 1, 1)}
        value = [min, max]
        return min, max, marks, value

#
# loader = DataLoader()
# print(loader.get_file_names())
# loop = asyncio.get_event_loop()
# loop.run_until_complete(loader.start())
# print('start')
# print(loader.load_file('BryanDataCenter_results'))
# print('second time much faster')
# print(loader.load_file('BryanDataCenter_results'))
#
