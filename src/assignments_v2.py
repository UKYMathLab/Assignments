import os
import itertools as it

import numpy as np
import pandas as pd

from utils import configs
from utils.preprocessing import preprocess
from Student import Student
from LabGroup import LabGroup
import utils.drivers as driver


def find_assignments():
    
    config = configs.AssignmentsConfig()

    # load the data
    students, lab_groups = preprocess(config.preprocess_config)
    
    # match students with lab group times for each lab group
    for lg in lab_groups:
        # assigns a student to each time it is available for each of the lab group's times
        lg.find_members(students)
    
    # get some order for the lab group (formally, a "combination")
    # this is the product thing from Nathan's proposal

    # find valid partitions from those

    # score based on happiness criteria

    # get best matching


if __name__ == '__main__':
    find_assignments()


