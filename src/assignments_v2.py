import os
import itertools as it
import collections

import numpy as np
import pandas as pd

from utils import configs
from utils.preprocessing import preprocess
from Student import Student
from LabGroup import LabGroup
import utils.drivers as driver


def _check_is_good_combo(student_combo: list, all_students: list, config) -> bool:
    r"""Checks if a given combination is valid.

    Criteria to check:
    (1) All students are accounted for
    (2) No student appears more than once
    (3) All lab groups have 3 <= num_members <= 5
    """

    is_good = []

    # all students are accounted for and no student is present more than once
    if set([*studs for studs in student_combo]) == set(all_students):
        #occurrences = collections.Counter(*student_combo)

        # all students occur only one time
        # if student is in more that one lab group for some tup, toss it out
        # there will eventually be a tuple with student in only one lab group
        #if max(occurrences.values() == 1):
        for lg_students in student_combo:
            if len(lg_students) in config.group_sizes:
                is_good.append(True)
            else:
                is_good.append(False)

    return (np.array(is_good)).all()


def find_assignments():

    config = configs.AssignmentsConfig()

    # load the data
    students, lab_groups = preprocess(config.preprocess_config)

    # match students with lab group times for each lab group
    for lg in lab_groups:
        lg.find_members(students)


    good_combos = {}
    cart_prod_lg_times = [list(lg.good_times.keys()) for lg in lab_groups]

    # I'm not sure if this product will work as coded (since input is list of lists)
    for idx, time_combo in enumerate(it.product(*cart_prod_lg_times)):
        lg_students = [lg.good_times[time_combo[i]] for i, lg in enumerate(lab_groups)]
        students_in_time_combo = [*studs for studs in lg_students]

        # all students accounted for
        if set(students_in_time_combo) == set(students):
            for group_size_combo in it.combinations_with_replacement(config.group_sizes, r=len(lab_groups)):

                # checksum
                if sum(group_size_combo) == len(students):
                    # list of lists of lists
                    all_student_combos = [it.combinations(lg_studs[i], r=group_size_combo[i]) for i, lg_studs in enumerate(lg_students)]

                    # check if every combination is compatible
                    for particular_student_combo in it.product(*all_student_combos):
                        if _check_if_good_combo(particular_student_combo, students):
                            good_combos[f"match{idx}"] = (time_combo, particular_student_combo)

    # check all found combinations
    for key, value in good_combos.items():
        print(f"{key}: {value}\n")

    # score based on happiness criteria

    # get best matching


if __name__ == '__main__':
    find_assignments()
