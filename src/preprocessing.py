import os
from pathlib import Path

import numpy as np
import pandas as pd

from Student import Student
from LabGroup import LabGroup
from utils import configs, drivers


def _load_file(file_path: Path, column_names: list) -> pd.DataFrame:
    r"""Loads a CSV into a Pandas DataFrame."""

    data = pd.read_csv(file_path, header=0, names=column_names)

    return data


def _format_times(sample: pd.DataFrame) -> set:
    r"""Gets times for each day and formats per row."""

    days_times = sample[["M_times", "T_times", "W_times", "Th_times", "F_times"]]

    times = []
    for day in days_times:
        # make sure there are available times
        if pd.notna(day):
            times += [*day.split(";")]

    return set(times)


def _format_preferences(sample: pd.DataFrame) -> list:
    r"""Organizes sample's preferences into an (ordered) list."""

    df_prefs = sample[["Pref1", "Pref2", "Pref3", "Pref4", "Pref5"]]

    return [pref for pref in df_prefs]


def preprocess(config):

    student_data = _load_file(file_path=config.student_data_path, column_names=config.student_column_names)
    lab_group_data = _load_file(file_path=config.lab_group_data_path, column_names=config.lab_group_column_names)

    # create and populate an array of Students
    students = [Student() for _ in student_data.index]
    for i, stud in enumerate(students):
        sample = student_data.iloc[i]

        stud.name = sample["Name"]
        stud.email = sample["Email"]

        stud.available_times = _format_times(sample)
        stud.preferences = _format_preferences(sample)
        #print(f'Student {stud.name}: {stud.preferences}\n')

    # create and populate an array of LabGroups
    lab_groups = [LabGroup() for _ in lab_group_data.index]
    for i, lg in enumerate(lab_groups):
        sample = lab_group_data.iloc[i]

        sample.name = sample["Name"]

    return students


if __name__ == '__main__':
    config = configs.PreprocessingConfig()

    students = preprocess(config)
