import os
from pathlib import Path

import numpy as np
import pandas as pd

import configs
import drivers

def _load_file(file_path: Path, column_names: list) -> pd.DataFrame:
    r"""Loads a CSV into a Pandas DataFrame."""

    data = pd.read_csv(file_path, header=0, names=column_names)

    return data


def preprocess(config):

    data = _load_file(config.data_file_path)


if __name__ == '__main__':
    config = configs.PreprocessingConfig()

    data = _load_file(file_path=config.data_path, column_names=config.column_names)
    drivers.ExamineData(data).pause()


