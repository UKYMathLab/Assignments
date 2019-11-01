import os
import argparse
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


def _score_configuration(combination, lab_groups):
    r"""Calculates the total unhappiness for a given configuration of lab groups.

    Calculated as the sum of the indexes into each student's preference list of
    their actual assignment.
    """


    # calculate the index offset for each student
    total_unhappiness = 0

    for i, lg_students in enumerate(combination):
        for stud in lg_students:
            total_unhappiness += stud.preferences.index(lab_groups[i])

    return total_unhappiness


def find_assignments(students, lab_groups, config):

    # match students with lab group times for each lab group
    for lg in lab_groups:
        lg.find_members(students)

    good_combos = []
    cart_prod_lg_times = [list(lg.good_times.keys()) for lg in lab_groups]

    # I'm not sure if this product will work as coded (since input is list of lists)
    for time_combo in enumerate(it.product(*cart_prod_lg_times)):
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
                            good_combos.append((time_combo, particular_student_combo))


    # check all found combinations
    for times, combos in good_combos:
        print(f"{times}   --->   {combos}\n")

    # score based on happiness criteria
    scores = [_score_configuration(lg_configurations, lab_groups) for (_, lg_configurations) in good_combos]

    # get best matching(s) and print results
    min_score = min(scores)
    best_scores_idx = [i for i, score in enumerate(scores) if score == min_score]

    print(f"Best Results (Unhappiness = {min_score})\n========================")
    for idx in best_scores_idx:
        print(f"{idx}:   {good_combos[idx][0]}   --->   {good_combos[idx][1]}\n")


if __name__ == "__main__":
    parser = argparser.ArgumentParser()
    parser.add_arguments("--gen_data", action="store_true", help="Generate fake data (as opposed to loading real data)")
    args = parser.parse_args()

    cfg = configs.AssignmentsConfig()

    student_data, lab_group_data = preprocess(cfg.preprocess_config)

    find_assignments(student_data, lab_group_data, cfg)
