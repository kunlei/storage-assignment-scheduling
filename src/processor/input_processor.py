import numpy as np
import pandas as pd

from src.common.frame import Frame
from src.common.picking_station import PickingStation
from src.common.storage_unit import StorageUnit

class InputProcessor:

    def __init__(self):
        pass

    def process(self, environment_file: str, order_file: str):
        # process environment
        env_df = pd.read_csv(environment_file, header=None, na_values='')
        env_df.fillna(2, inplace=True)
        env_df.replace(to_replace='PS1', value=-1, inplace=True)
        env_df.replace(to_replace='PS2', value=-2, inplace=True)
        env_df = env_df.astype('int')
        num_rows, num_cols = env_df.shape
        print(num_rows)
        print(num_cols)
        print(env_df)

        stations = []
        env = np.empty(shape=(num_rows, num_cols), dtype=StorageUnit)
        for row_idx in range(num_rows):
            for col_idx in range(num_cols):
                val = env_df.iloc[row_idx, col_idx]
                unit = StorageUnit(row_idx, col_idx, val)
                env[row_idx, col_idx] = unit

                if val == -1:
                    station = PickingStation(1, row_idx, col_idx)
                    stations.append(station)
                elif val == -2:
                    station = PickingStation(2, row_idx, col_idx)
                    stations.append(station)



        # process order lines
        orders = pd.read_csv(order_file, parse_dates=True, date_format='%Y-%m-%d_%H:%M:%S')
        orders.columns = ['arrival', 'departure', 'frame', 'station']
        orders.sort_values(by=['arrival', 'departure'], inplace=True)
        print(orders)
