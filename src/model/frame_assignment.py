import numpy as np

from src.common.data_center import DataCenter
from src.common.storage_unit import StorageUnit
from src.common.unit_type import UnitType
from src.common.picking_station import PickingStation

from ortools.linear_solver import pywraplp

import random


class FrameAssignment:

    def __init__(self, data_center):
        self._data_center: DataCenter = data_center

    def optimize(self, order_batch: list):
        # collect the scheduling requests for each frame to each picking station
        # frame + picking station -> count
        frame_requests: dict = {}
        for order in order_batch:
            frame = order.frame_id
            if frame not in frame_requests:
                frame_requests[frame] = {1: 0, 2: 0}
            station_dict = frame_requests[frame]
            station = order.station_id
            station_dict[station] = station_dict[station] + 1

        # all the frames
        frames = self._data_center.frames

        # create solver
        solver = pywraplp.Solver.CreateSolver('SCIP')

        # create decision variables
        env = self._data_center.env
        num_rows, num_cols = env.shape
        var_assign = {}
        var_move = {}
        for frame in frames:
            var_assign[frame] = np.empty((num_rows, num_cols), dtype=object)
            var_move[frame] = np.empty((num_rows, num_cols), dtype=object)
        for f in frames:
            for row in range(num_rows):
                for col in range(num_cols):
                    var_assign[f][row][col] = solver.BoolVar(name=f"x_{f},{row},{col}")
                    var_move[f][row][col] = solver.BoolVar(name=f"y_{f},{row},{col}")

        # create objective function
        stations: list[PickingStation] = self._data_center.stations
        obj_expr = []
        for f in frame_requests:
            picking_requests = frame_requests[f]
            for row in range(num_rows):
                for col in range(num_cols):
                    for station in stations:
                        distance = abs(station.row_idx - row) + abs(station.col_idx - col)
                        requests = picking_requests[station.id]
                        obj_expr.append(var_assign[f][row][col] * distance * requests)
        alpha = 1.0
        for f in frames:
            for row in range(num_rows):
                for col in range(num_cols):
                    obj_expr.append(alpha * var_move[f][row][col])
        solver.Minimize(solver.Sum(obj_expr))

        # constraint: each frame must be assigned to a storage unit
        for f in frames:
            constr_expr = [
                var_assign[f][row][col]
                for row in range(num_rows)
                for col in range(num_cols)
                if env[row][col].type == UnitType.STORAGE
            ]
            solver.Add(solver.Sum(constr_expr) == 1)

        # constraint: there can be at most one frame in a storage unit
        for row in range(num_rows):
            for col in range(num_cols):
                if env[row][col].type == UnitType.STORAGE:
                    constr_expr = [
                        var_assign[f][row][col]
                        for f in frames
                    ]
                    solver.Add(solver.Sum(constr_expr) <= 1)

        # derive move variables
        frame_assignments = self._data_center.frame_assignments
        for f in frames:
            curr_row, curr_col = frame_assignments[f]
            for row in range(num_rows):
                for col in range(num_cols):
                    exists = 1 if (row == curr_row) and (col == curr_col) else 0
                    solver.Add(var_move[f][row][col] >= exists - var_assign[f][row][col])
                    solver.Add(var_move[f][row][col] >= var_assign[f][row][col] - exists)

        # solve
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            print('re-assignment problem solved successfully!')
            print(f"optimal solution value = {solver.Objective().Value()}")

            new_frame_assignments = {}
            for frame in frames:
                for row in range(num_rows):
                    for col in range(num_cols):
                        if var_assign[frame][row][col].solution_value() > 0.99:
                            new_frame_assignments[frame] = (row, col)
            old_frame_assignments = self._data_center.frame_assignments
            print(f"show changed frame positions: ")
            for frame in frames:
                if new_frame_assignments[frame] != old_frame_assignments[frame]:
                    print(f"frame: {frame}: position change: {old_frame_assignments[frame]} -> {new_frame_assignments[frame]}")

            self._data_center.frame_assignments = new_frame_assignments

            for frame in new_frame_assignments:
                row, col = new_frame_assignments[frame]
                env[row][col].frame = frame
            print(f"show storage plans: ")
            print(new_frame_assignments)
            print("\n\n\n")

    def init_frame_assignment(self) -> None:
        """
        this function randomly assigns a frame into an available storage unit
        """
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
