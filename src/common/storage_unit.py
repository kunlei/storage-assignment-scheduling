from src.common.unit_type import UnitType


class StorageUnit:

    def __init__(self, row_idx, col_idx, type):
        self._row_idx = row_idx
        self._col_idx = col_idx
        self._type = None
        if type == 0:
            self._type = UnitType.MOVE
        elif type == 1:
            self._type = UnitType.STORAGE
        elif type == 2:
            self._type = UnitType.OBSTACLE
        elif type < 0:
            self._type = UnitType.STATION

        self._frame = -1

    @property
    def row_idx(self) -> int:
        return self._row_idx

    @property
    def col_idx(self) -> int:
        return self._col_idx

    @property
    def type(self) -> UnitType:
        return self._type

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    def __str__(self):
        return f"({self._row_idx}, {self._col_idx}, {self._type})"
