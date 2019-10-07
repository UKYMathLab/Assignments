import os
import os.path as p

import numpy as np
import pandas as pd



def _load_file(file_path: str) -> pd.DataFrame:
    r"""Loads a CSV into a Pandas DataFrame."""

    data = pd.read_csv(file_path)

    return data

def _rename_columns(data: pd.DataFrame) -> pd.DataFrame:
    r"""Renames the columns of the DataFrame to meaningful names."""

    pass
   

