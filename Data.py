from tqdm import tqdm
from decimal import Decimal
from typing import Iterator
from sortedcontainers import SortedDict
from collections import deque, defaultdict
import os
import glob
import pandas as pd
import pickle
from time import time

class Simulator:
    def __init__(self,
                match_id: str,
                base='/Users/lihaohan/Desktop/ubiq-data-master'):
        self.base = base
        self.match_path = os.path.join(self.base, match_id)
        self.codes = ['UBIQ{:03d}'.format(i) for i in range(50)]
        self.bid_price_path = os.path.join(self.match_path, 'bid', 'price')
        self.bid_volume_path = os.path.join(self.match_path, 'bid', 'volume')
        self.ask_price_path = os.path.join(self.match_path, 'ask', 'price')
        self.ask_volume_path = os.path.join(self.match_path, 'ask', 'volume')

        self.Days = [day for day in os.listdir(self.bid_price_path) if day != '.DS_Store']

        self.output_data = os.path.join(self.match_path, 'all')
        if not os.path.exists(self.output_data):
            os.makedirs(self.output_data)

        self.data_files = []

    def _pooled_single_stock(self, code: str, date: str):
        paths = [(self.bid_price_path, '_price'), (self.bid_volume_path, '_volume'), 
             (self.ask_price_path, '_price'), (self.ask_volume_path, '_volume')]
        try:
            data = pd.concat([pd.read_pickle(os.path.join(path, date, code+'.pkl')).add_suffix(suffix) for path, suffix in paths], axis=1)
            with open(os.path.join(self.output_data, date+'_'+code+'.pkl'), 'wb') as f:
                pickle.dump(data, f)
        except:
            print(f'Some error occured in pooling {code} in {date}')

    def _pooled_all_stock(self):
        for day in self.Days:
            for code in self.codes:
                self._pooled_single_stock(code, day)

    def _load_data_files(self):
        """
        Iterate through all the stock data files in the base directory, storing the file path in the list.
        """
        try:
            self.data_files = glob.glob(os.path.join(self.output_data, '*.pkl'))
        except:
            print('Please run the _pooled_all_stock function first')

    def _data_generator(self):
        """
        Returns a generator that reads the contents of all data files line by line.
        """
        iterators = [(os.path.basename(file_path).split('_')[1].split('.')[0], pd.read_pickle(file_path).iterrows(), []) for file_path in self.data_files]
        print(f'Created {len(iterators)} iterators.')

        while True:
            try:
                data = {}
                for stock_name, iterator, rows in iterators:
                    row = next(iterator)[1]
                    rows.append(row.to_dict())
                    data[stock_name] = pd.DataFrame(rows)
                print(f'Yielding data: {data}')
                yield data
            except StopIteration:
                break


