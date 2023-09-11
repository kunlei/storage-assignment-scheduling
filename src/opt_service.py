import pandas as pd
import os

from src.processor.input_processor import InputProcessor
from src.processor.output_processor import OutputProcessor
from src.model.frame_assignment import FrameAssignment
from src.common.data_center import DataCenter


class OptService:

    def __init__(self):
        self._input_processor = InputProcessor()
        self._output_processor = OutputProcessor()
        self._frame_assignment = None

    def optimize(self, environment_file, order_file):
        # process input data
        data_center = self._input_processor.process(environment_file, order_file)

        # initialize frame assignments
        self._frame_assignment = FrameAssignment(data_center)
        self._frame_assignment.init_frame_assignment()

        # optimize
        start_idx: int = 0
        orders = data_center.orders
        count = 500
        while start_idx <= len(orders):
            order_batch = data_center.get_order_batch(start_idx, count)
            self._frame_assignment.optimize(order_batch)
            start_idx += count

        # process output

        pass
