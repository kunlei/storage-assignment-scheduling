

class PickingStation:

    def __init__(self, station_id, row_idx, col_idx):
        self._id = station_id
        self._row_idx = row_idx
        self._col_idx = col_idx

    @property
    def id(self):
        return self._id

    @property
    def row_idx(self):
        return self._row_idx

    @property
    def col_idx(self):
        return self._col_idx