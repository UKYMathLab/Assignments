import os
import argparse
import itertools as it
import collections
import multiprocessing as mp

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


def _check_is_good_combo_wrapper(args):
    return _check_is_good_combo(*args)


def _check_all_combos(time_combination, student_combinations, all_students, config):
    r"""Checks if all combinations are valid."""

    good_combos = []
    for particular_student_combination in it.product(*student_combinations):
        if _check_is_good_combo(particular_student_combination, all_students, config):
            good_combos.append((time_combination, particular_student_combination))
    

def _check_all_combos_wrapper(args):
    return _check_all_combos(*args)


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


if __name__ == "__main__":
    cfg = configs.AssignmentsConfig()

    # read the student and lab group data and load into objects
    students, lab_groups = preprocess(cfg.preprocess_config)
    
    # find student assignments to lab groups
    # match students with lab group times for each lab group
    for lg in lab_groups:
        lg.find_members(students)

    all_good_combos = []
    cart_prod_lg_times = [list(lg.good_times.keys()) for lg in lab_groups]

    # iterate over all possible combinations
    all_time_combos_pbar = tqdm(list(it.product(*cart_prod_lg_times)), desc="Going through time combinations")
    for time_combo in all_time_combos_pbar:
        lg_students = [lg.good_times[time_combo[i]] for i, lg in enumerate(lab_groups)] # list of sets of students
        students_in_time_combo = [stud for studs in lg_students for stud in studs]

        # all students accounted for
        if set(students_in_time_combo) == set(students):
            for group_size_combo in it.combinations_with_replacement(cfg.group_sizes, r=len(lab_groups)):
                # checksum
                if sum(group_size_combo) == len(students):
                    all_student_combos = [it.combinations(lg_studs, r=group_size_combo[i]) for i, lg_studs in enumerate(lg_students)]

                    # check if every combination is compatible

                    available_cpus = mp.cpu_count()
                    print(f"cpus: {available_cpus}")
                    with mp.Pool(available_cpus) as p:
                        print("Got into the MP pool!")
                        all_student_combos_prod = list(it.product(*all_student_combos))
                        print("Got past the product!")
                        results = [p.apply_async(_check_is_good_combo, (particular_student_combo, students, cfg)).get() for particular_student_combo in all_student_combos_prod]
                        print("Got past the async!")
                        print(f"Results: {results}")
                        # find good combinations
                        for student_combo, result in zip(all_student_combos_prod, results):
                            print("Going through the combinations to find the good ones!")
                            if result:
                                print(f"Found a combination!")
                                all_good_combos.append(student_combo)
                                print(f"result: {result}")
                                print(f"all_good_combos: {all_good_combos}\n\n")

        all_time_combos_pbar.update()
        all_time_combos_pbar.refresh()

    # record all found combinations and compute scores
    _write_good_combos(all_good_combos, cfg.preprocess_config.data_dir/"all_configurations.txt", lab_groups)
    scores = [_score_configurations(lg_configurations, lab_groups) for (_, lg_configurations) in all_good_combos]
    
    # get best matching(s) and record results
    min_score = min(scores)
    best_scores_idx = [i for i, score in enumerate(scores) if score == min_score]
    best_combos = [all_good_combos[i] for i in best_scores_idx]
    _write_good_combos(best_combos, cfg.preprocess_config.data_dir/"best_configurations.txt", lab_groups, write_score=True, score=min_score)

    # indicate that script is finished
    with open(cfg.preprocess_config.data_dir/"finished.txt", "w") as finish_file:
        finish_file.write("Finished!")
