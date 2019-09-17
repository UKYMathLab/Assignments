import os
import pandas as pd
import numpy as np

from utils.configs import AssignmentsConfig
import utils.drivers as drivers

################################################################################

def _load_data(config) -> pd.DataFrame:
    r"""Loads an Excel spreadsheet into a Pandas DatFrame.

    :param config:
        contains higher-level information such as paths
    :return data: pd.DataFrame
        the loaded spreadsheet
    """

    data = pd.read_excel(config.data_path, header=None, skiprows=1,
                         names=config.column_names)
    return data


def main():

    config = AssignmentsConfig()

    data = _load_data(config)

    return data

################################################################################

if __name__ == '__main__':
    data = main()
    drivers.ExamineData(data).pause()
    drivers.ShowSample(data).pause()
