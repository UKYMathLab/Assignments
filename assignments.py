import os
import pandas as pd
import numpy as np

from utils.configs import AssignmentsConfig
from Student import Student
from LabGroup import LabGroup
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

    lab_groups = [LabGroup() for _ in range(num_groups)]
    students = [Student() for _ in range(num_students)]

    # check if student and lab group are compatible
    for student in students:
        for group in lab_groups:
            # times are compatible so add the student to the lab group
            if len(person.available_times.intersect(group.available_times)) >= 1:
                group.possible_group_members.append(student)

    for group in range(lab_groups):
        three_combos = itertools.combinations(group.possible_group_members, 3)
        for combo in three_combos:
            if len(combo[0].available_times.intersect(combo[1].available_times.intersect(combo[2].available_times))) >= 1:
                group.three_student_combos.append(set(combo))

    four_combos = itertools.combinations(group.possible_group_members, 4)
    for combo in four_combos:
        if len(combo[0].available_times.intersect(combo[1].available_times.intersect(combo[2].available_times.intersect(combo[3].available_times)))) >= 1:
            group.four_student_combos.append(set(combo))

    five_combos = itertools.combinations(group.possible_group_members, 5)
    for combo in five_combos:
        if len(combo[0].available_times.intersect(combo[1].available_times.intersect(combo[2].available_times.intersect(combo[3].available_times.intersect(combo[4].available_times))))) >= 1:
            group.five_student_combos.append(set(combo))

    return data

################################################################################

if __name__ == '__main__':
    data = main()
    drivers.ExamineData(data).pause()
    drivers.ShowSample(data).pause()
