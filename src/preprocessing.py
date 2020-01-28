from pathlib import Path

import pandas as pd

from utils import Student, LabGroup
from utils import PreprocessingConfig


def _load_file(file_path: Path, column_names: list) -> pd.DataFrame:
    r"""Loads a CSV into a Pandas DataFrame."""

    data = pd.read_csv(file_path, header=0, names=column_names)

    return data


def _format_times(sample: pd.DataFrame, config: PreprocessingConfig) -> set:
    r"""Gets times for each day and formats per row."""

    days_times = sample[["M_times", "T_times", "W_times", "Th_times", "F_times"]]

    times = []
    for day in days_times:
        # make sure there are available times
        if pd.notna(day):
            times += [*day.split(config.csv_sep)]

    return set(times)


def _format_preferences(sample: pd.DataFrame) -> list:
    r"""Organizes sample's preferences into an (ordered) list."""

    df_prefs = sample[["Pref1", "Pref2", "Pref3", "Pref4", "Pref5"]]

    return [pref for pref in df_prefs]


def preprocess(config):

    student_data = _load_file(file_path=config.student_data_file, column_names=config.student_column_names)
    lab_group_data = _load_file(file_path=config.lab_group_data_file, column_names=config.lab_group_column_names)

    # create and populate an array of Students
    students = [Student() for _ in student_data.index]
    for i, stud in enumerate(students):
        sample = student_data.iloc[i]

        stud.name = sample["Name"]
        stud.email = sample["Email"]

        stud.available_times = _format_times(sample, config)
        stud.preferences = _format_preferences(sample)

    # create and populate an array of LabGroups
    lab_groups = [LabGroup() for _ in lab_group_data.index]
    for i, lg in enumerate(lab_groups):
        sample = lab_group_data.iloc[i]

        if config.file_format == "F_2019":
            lg.name = sample["Name"]
        elif config.file_format == "S_2020":
            lg.name = config.group_map[sample["Name"]]
        else:
            raise NotImplementedError(f"The {config.file_format} file format has not been implemented yet!")

        lg.available_times = _format_times(sample, config)

    return students, lab_groups


if __name__ == '__main__':
    cfg1 = PreprocessingConfig(student_data_file="RealishStudentData.csv", lab_group_data_file="FakeLabGroupData.csv",
                               file_format="F_2019")
    cfg2 = PreprocessingConfig(student_data_file="student_sample.csv", lab_group_data_file="faculty_sample.csv",
                               file_format="S_2020")

    for cfg in [cfg1, cfg2]:
        print(f"{cfg.file_format}\n==========")
        studs, lgs = preprocess(cfg)

        for stud in studs:
            print(f"{stud.name}: {stud.available_times}\n{stud.preferences}")
        print("\n"*5)
        for lg in lgs:
            print(f"{lg.name}: {lg.available_times}\n")

        print("\n"*3)