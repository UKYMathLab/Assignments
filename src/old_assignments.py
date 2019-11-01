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

    # find all compatible k-people groups for each group
    for group in range(lab_groups):
        three_combos = itertools.combinations(group.possible_group_members, 3)
        three_student_combos = []
        four_student_combos = []
        five_student_combos = []

        for combo in three_combos:
            if len(combo[0].available_times.intersect(combo[1].available_times, combo[2].available_times)) >= 1:
                three_student_combos.append(set(combo))

        four_combos = itertools.combinations(group.possible_group_members, 4)
        for combo in four_combos:
            if len(combo[0].available_times.intersect(combo[1].available_times, combo[2].available_times, combo[3].available_times)) >= 1:
                four_student_combos.append(set(combo))

        five_combos = itertools.combinations(group.possible_group_members, 5)
        for combo in five_combos:
            if len(combo[0].available_times.intersect(combo[1].available_times, combo[2].available_times, combo[3].available_times, combo[4].available_times)) >= 1:
                five_student_combos.append(set(combo))

        # check that combinations are nonempty
        if three_student_combos:
            group.possible_groups[3] = three_student_combos
        if four_student_combos:
            group.possible_groups[4] = four_student_combos
        if five_student_combos:
            group.possible_groups[5] = five_student_combos

    # generate all possible combinations of k-element groups
    possible_sizes = [3, 4, 5]
    all_group_size = [possible_sizes for i in range(5)]



    # find all combinations of groups that have have all students in them



    return data

################################################################################

if __name__ == '__main__':
    data = main()
    drivers.ExamineData(data).pause()
    drivers.ShowSample(data).pause()
