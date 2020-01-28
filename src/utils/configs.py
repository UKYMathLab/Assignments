from pathlib import Path
from typing import Union


def find_path(desired: Union[str, Path], max_levels: int = 3):
    r"""Searches for a desired directory or file.

    Searches recursively for a desired file given an initial
    starting path and the maximum number of parent directory
    levels to search from.
    """

    try:
        start_path = [p for p in Path().cwd().parents if p.name == "Assignments"][0]
    except FileNotFoundError:
        raise FileNotFoundError("Cannot find Assignments directory.")

    found_paths = list(start_path.rglob(desired))
    if len(found_paths) <= 0:
        raise FileNotFoundError(f"Cannot find {desired} from {start_path}")
    else:
        found_path = found_paths[0]

    return found_path


class PreprocessingConfig:
    def __init__(self, student_data_file: Union[str, Path], lab_group_data_file: Union[str, Path],
                 file_format: str = "F_2019"):
        r"""
        :param student_data_file: Union[str, Path]
            Either the name of the student data file or a Path to the student data file.
        :param lab_group_data_file: Union[str, Path]
            Either the name of the lab group data file or a Path to the lab group data file.
        :param file_format: str
            Determines how to parse the given CSV's. Currently implemented for files from
            Fall 2019 ("F_2019") and Spring 2020 ("S_2020").
            (default="F_2019")
        """

        # paths
        self.data_dir = find_path(desired="data")
        self.student_data_file = find_path(desired=student_data_file)
        self.lab_group_data_file = find_path(desired=lab_group_data_file)

        # formatting data
        self.file_format = file_format
        if self.file_format == "F_2019":
            self.student_column_names = ["Timestamp", "Name", "Email",
                                         "Pref1", "Pref2", "Pref3", "Pref4", "Pref5",
                                         "M_times", "T_times", "W_times", "Th_times", "F_times"]
            self.lab_group_column_names = ["Timestamp", "Name",
                                           "M_times", "T_times", "W_times", "Th_times", "F_times"]
            self.group_map = None
            self.csv_sep = ";"

        elif self.file_format == "S_2020":
            self.student_column_names = ["Timestamp", "Name", "Email", "Previous Group(s)", "Visualization",
                                         "Pref1", "Pref2", "Pref3", "Pref4", "Pref5",
                                         "M_times", "T_times", "W_times", "Th_times", "F_times",
                                         "Course Credit", "Additional Comments"]
            self.lab_group_column_names = ["Timestamp", "Name",
                                           "M_times", "T_times", "W_times", "Th_times", "F_times",
                                           "Additional Comments"]
            self.group_map = {"Kate ": "[Ponto - Assignments]",
                              "Manon": "[Manon - Heisenberg]",
                              "Max Kutler": "[Kutler - Matroids]",
                              "Dave": "[Jensen - Brambles and Scrambles]",
                              "Khrystyna Serhiyenko": "[Serhiyenko - Cluster Variables]"}
            self.csv_sep = ", "

        else:
            raise NotImplementedError(f"The {self.file_format} file format has not been implemented yet!")


class AssignmentsConfig(PreprocessingConfig):
    def __init__(self, min_size: int = 3, max_size: int = 5, **kwargs):
        super(AssignmentsConfig, self).__init__(**kwargs)
        self.group_sizes = list(range(min_size, max_size+1))


if __name__ == "__main__":
    config = AssignmentsConfig(student_data_file="RealishStudentData.csv", lab_group_data_file="FakeLabGroupData.csv",
                               file_format="F_2019")

    print(f"Data directory: {config.data_dir}")
    print(f"Student data file path: {config.student_data_file}")
    print(f"Lab group data file path: {config.lab_group_data_file}")
