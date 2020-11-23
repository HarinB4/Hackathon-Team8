import os
import pandas as pd
import asyncio
from threading import Thread

import time


# This class will handle loading the csv files
class DataLoader(Thread):
    files = None
    data = None
    file_names = None
    DIR = '../data/Analysis/'
    DIR2 = '../data/'
    label_file = 'Meter Names and Labels.xlsx'
    meters = None
    files = [file for file in os.listdir(DIR) if file.endswith('.csv')]
    # turn filename.csv to filename for all files
    file_names = [os.path.splitext(os.path.basename(x))[0] for x in files]
    file_names.sort()
    data = {}
    meters = pd.read_excel(DIR2 + label_file, 'Sheet1')
    meters['Name'] = meters['Name'].str.replace('\'', "").str.strip()

    def run(self):
        # this function loads all data in the Analysis directory
        if self.data == {}:
            for i in range(len(self.file_names)):
                try:
                    self.data[self.file_names[i]] = pd.read_csv(self.DIR + self.files[i], parse_dates=['Datetime'])
                except FileNotFoundError:
                    self.data[self.file_names[i]] = pd.DataFrame()
                time.sleep(3)

    def load_file(self, file_name) -> pd.DataFrame:
        # this function loads a single specified file
        try:
            if file_name in self.data:
                if len(self.data[file_name]) != 0:
                    return self.data[file_name]
            else:
                self.data[file_name] = pd.read_csv(self.DIR + file_name + '_results.csv', parse_dates=['Datetime'],
                                                   date_parser=lambda col: pd.to_datetime(col, utc=True),
                                                   index_col='Datetime')
                return self.data[file_name]
        except FileNotFoundError:
            return pd.DataFrame([])

    def get_file_names(self):
        # this function returns a list of file names
        return self.file_names

    def get_labels(self):
        return self.meters
