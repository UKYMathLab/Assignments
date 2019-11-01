import os
from pathlib import Path


def find_data_dir(path: Path, desired_dir="data"):
    # find data directory by searching hierarchy of directories
    # should find "data" directory
    max_levels = 3

    i = 0
    while i < max_levels:
        # "data" directory is found
        if path / desired_dir in path.iterdir():
            path = path / desired_dir
            i = max_levels + 1   # condition found, break out of while
        # move up a directory
        else:
            i += 1
            path = path.parent    # try again, but one directory up

        # don't check too far up hierarchy
        if i == max_levels:
            print("Can't find data directory.\n")

    return path


class PreprocessingConfig:
    def __init__(self):
        # paths
        self.data_dir = find_data_dir(Path().cwd(), desired_dir="data")
        self.student_data_file_name = "FakeStudentData.csv"
        self.lab_group_data_file_name = "FakeLabGroupData.csv"

        # formatting data
        self.student_column_names = ["Timestamp", "Name", "Email",
                                     "Pref1", "Pref2", "Pref3", "Pref4", "Pref5",
                                     "M_times", "T_times", "W_times", "Th_times", "F_times"]
        self.lab_group_column_names = ["Timestamp", "Name",
                                       "M_times", "T_times", "W_times", "Th_times", "F_times"]

    @property
    def student_data_path(self):
        return self.data_dir / self.student_data_file_name

    @property
    def lab_group_data_path(self):
        return self.data_dir / self.lab_group_data_file_name


class AssignmentsConfig:
    def __init__(self, min_size: int=3, max_size: int=5):
        self.preprocess_config = PreprocessingConfig()

        self.group_sizes = list(range(min_size, max_size+1))


if __name__ == "__main__":
    config = PreprocessingConfig()

    print(f"Data directory: {config.data_dir}")
