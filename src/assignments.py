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
    (2) No student appears more than once (already checked by (1))
    (3) All lab groups have 3 <= num_members <= 5 (true by assumption from code before)
    """

    is_good = False

    # all students are accounted for and no student is present more than once
    if set([stud for studs in student_combo for stud in studs]) == set(all_students):
        is_good = True

    return is_good


def _write_good_combos(good_combos: list, file_name, lab_groups, write_score: bool=False, score: int=0):
    r"""Writes the given time/student configurations to a specified .txt file."""

    with open(file_name, "w") as f:
        if write_score:
            f.write(f"Unhappiness level: {score}\n")
        for i, (times, combos) in enumerate(good_combos):
            title = f"Configuration {i+1}"
            f.write(f"{title}\n" + ("="*len(title)) + "\n")

            for j, (time, combo) in enumerate(zip(times, combos)):
                f.write(f"{lab_groups[j].name} ({time}): ")

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

    # I'm not sure if this product will work as coded (since input is list of lists)
    all_time_combos_pbar = tqdm(list(it.product(*cart_prod_lg_times)), desc="Going through time combinations")
    for time_combo in all_time_combos_pbar:
        lg_students = [lg.good_times[time_combo[i]] for i, lg in enumerate(lab_groups)]     # list of sets of students
        students_in_time_combo = [stud for studs in lg_students for stud in studs]

        # all students accounted for
        if set(students_in_time_combo) == set(students):
            for group_size_combo in it.combinations_with_replacement(config.group_sizes, r=len(lab_groups)):
                # checksum
                if sum(group_size_combo) == len(students):
                    all_student_combos = [it.combinations(lg_studs, r=group_size_combo[i]) for i, lg_studs in enumerate(lg_students)]   # list of lists of lists

                    # check if every combination is compatible
                    for particular_student_combo in it.product(*all_student_combos):

                        if _check_is_good_combo(particular_student_combo, students, config):
                            good_combos.append((time_combo, particular_student_combo))
        all_time_combos_pbar.update()
        all_time_combos_pbar.refresh()

    # record all found combinations and compute scores
    _write_good_combos(good_combos, config.preprocess_config.data_dir/"all_configurations.txt", lab_groups)
    scores = [_score_configuration(lg_configurations, lab_groups) for (_, lg_configurations) in good_combos]

    # get best matching(s) and record results
    min_score = min(scores)
    best_scores_idx = [i for i, score in enumerate(scores) if score == min_score]
    best_combos = [good_combos[i] for i in best_scores_idx]
    _write_good_combos(best_combos, config.preprocess_config.data_dir/"best_configurations.txt", lab_groups, write_score=True, score=min_score)


if __name__ == "__main__":
    cfg = configs.AssignmentsConfig()

    student_data, lab_group_data = preprocess(cfg.preprocess_config)

    find_assignments(student_data, lab_group_data, cfg)

    with open(cfg.preprocess_config.data_dir/"finished.txt", "w") as finish_file:
        finish_file.write("Finished!")
