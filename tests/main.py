import os
import numpy as np
import pandas as pd
from src.opt_service import OptService

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data_dir = "/Users/klian/dev/learn/python/storage-assignment-scheduling/tests/data"
    order_file = os.path.join(data_dir, "order_data.csv")
    environment_file = os.path.join(data_dir, "environment.csv")

    opt_service = OptService()
    opt_service.optimize(environment_file, order_file)
