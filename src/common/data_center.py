import numpy as np

class DataCenter:

    def __init__(self, env, stations, orders):
        self._env: np.array = env
        self._stations: list = stations
        self._orders: list = orders

        self._frames: set = set(order.frame_id for order in self._orders)
        self._frame_assignments: dict = {}

    @property
    def env(self):
        return self._env

    @property
    def stations(self):
        return self._stations

    @property
    def orders(self):
        return self._orders

    @property
    def frames(self) -> set:
        return self._frames

    @property
    def frame_assignments(self) -> dict:
        return self._frame_assignments

    def get_order_batch(self, start_idx: int, count: int) -> list:
        res = []
        for idx in range(start_idx, min(start_idx + count, len(self._orders))):
            res.append(self._orders[idx])
        return res
