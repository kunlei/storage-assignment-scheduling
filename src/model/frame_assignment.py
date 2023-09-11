from src.common.data_center import DataCenter
from src.common.storage_unit import StorageUnit
from src.common.unit_type import UnitType

import random


class FrameAssignment:

    def __init__(self, data_center):
        self._data_center: DataCenter = data_center

    def optimize(self):
        pass

    def init_frame_assignment(self):
        env = self._data_center.env
        num_rows, num_cols = env.shape
        frames = self._data_center.frames
        frame_assignments = self._data_center.frame_assignments

        random.seed(42)
        for frame in frames:
            assigned = False
            while not assigned:
                row_idx = random.randint(0, num_rows - 1)
                col_idx = random.randint(0, num_cols - 1)
                unit: StorageUnit = env[row_idx, col_idx]
                if unit.type is not UnitType.STORAGE:
                    continue
                if unit.frame < 0:
                    unit.frame = frame
                    frame_assignments[frame] = (row_idx, col_idx)
                    assigned = True
