import os
import argparse
import itertools as it
import collections

import numpy as np
import pandas as pd
from tqdm import tqdm

from utils import configs
from preprocessing import preprocess
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
    if set([stud for studs in student_combo for stud in studs]) == set(all_students):
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


def _write_good_combos(good_combos: list, file_name, lab_groups):

    with open(file_name, "w") as f:
        for i, (times, combos) in enumerate(good_combos):
            title = f"Configuration {i}"
            f.write(f"{title}\n" + ("="*len(title)) + "\n")

            for j, (time, combo) in enumerate(zip(times, combos)):
                f.write(f"{lab_groups[i].name} ({time}): ")

                for stud in combo:
                    f.write(f" {stud.name}")
                f.write("\n")
            f.write("\n"*4)


def _score_configuration(combination, lab_groups):
    r"""Calculates the total unhappiness for a given configuration of lab groups.

    Calculated as the sum of the indexes into each student's preference list of
    their actual assignment.
    """

    # calculate the index offset for each student
    total_unhappiness = 0

    for i, lg_students in enumerate(combination):
        for stud in lg_students:
            total_unhappiness += stud.preferences.index(lab_groups[i].name)

    return total_unhappiness


def find_assignments(students, lab_groups, config):

    # match students with lab group times for each lab group
    for lg in lab_groups:
        lg.find_members(students)

    good_combos = []
    cart_prod_lg_times = [list(lg.good_times.keys()) for lg in lab_groups]
    # for elem in cart_prod_lg_times: print(f"number of times: {len(elem)}   --->   {elem}\n")
    # for elem in cart_prod_lg_times: print(f"\n{elem}\n")
    # I'm not sure if this product will work as coded (since input is list of lists)
    all_time_combos_pbar = tqdm(list(it.product(*cart_prod_lg_times)), desc="Going through time combinations")
    for time_combo in all_time_combos_pbar:
        lg_students = [lg.good_times[time_combo[i]] for i, lg in enumerate(lab_groups)]     # list of sets of students
        students_in_time_combo = [stud for studs in lg_students for stud in studs]

        # for i, elem in enumerate(students_in_time_combo): print(i, elem)
        # print()
        # for i, elem in enumerate(set(students_in_time_combo)): print(i, elem)

        # all students accounted for
        if set(students_in_time_combo) == set(students):
            for group_size_combo in it.combinations_with_replacement(config.group_sizes, r=len(lab_groups)):
                # print(f"{group_size_combo} =?= {len(students)}")
                # checksum
                if sum(group_size_combo) == len(students):
                    all_student_combos = [it.combinations(lg_studs, r=group_size_combo[i]) for i, lg_studs in enumerate(lg_students)]   # list of lists of lists
                    filter_student_combos = [student_combo for student_combo in all_student_combos if set([stud for studs in student_combo for stud in studs]) == set(students)]
                    # print(len(filter_student_combos))
                    # print(f"Total permutations: {len(list(all_student_combos[0]))} x {len(list(all_student_combos[1]))} x {len(list(all_student_combos[2]))} x {len(list(all_student_combos[3]))} x {len(list(all_student_combos[4]))}")
                    # check if every combination is compatible
                    # all_student_combos_for_time_pbar = tqdm(list(it.product(*all_student_combos)), desc="Going through student configurations", leave=False)
                    for particular_student_combo in it.product(*filter_student_combos):
                        if _check_is_good_combo(particular_student_combo, students, config):
                            good_combos.append((time_combo, particular_student_combo))
                        # all_student_combos_for_time_pbar.update()
        all_time_combos_pbar.update()



    # record all found combinations
    _write_good_combos(good_combos, config.preprocessing_config.data_dir/"results.txt", lab_groups)

    # score based on happiness criteria
    scores = [_score_configuration(lg_configurations, lab_groups) for (_, lg_configurations) in good_combos]

    # get best matching(s) and print results
    min_score = min(scores)
    best_scores_idx = [i for i, score in enumerate(scores) if score == min_score]

    print(f"Best Results (Unhappiness = {min_score})\n========================")
    for idx in best_scores_idx:
        print(f"{idx}:   {good_combos[idx][0]}   --->   {good_combos[idx][1]}\n")


if __name__ == "__main__":
    cfg = configs.AssignmentsConfig()

    student_data, lab_group_data = preprocess(cfg.preprocess_config)

    find_assignments(student_data, lab_group_data, cfg)
