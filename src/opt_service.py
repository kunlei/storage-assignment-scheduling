import pandas as pd

from src.processor.input_processor import InputProcessor
from src.processor.output_processor import OutputProcessor
from src.model.frame_assignment import FrameAssignment


class OptService:

    def __init__(self):
        self._input_processor = InputProcessor()
        self._output_processor = OutputProcessor()
        self._frame_assignment = FrameAssignment()

    def optimize(self, environment: pd.DataFrame, orders: pd.DataFrame):
        # process input data
        self._input_processor.process(environment, orders)

        # optimize

        # process output

        pass
