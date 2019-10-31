import os
from pathlib import Path

    
def find_data_dir(path: Path):
    # find data directory by searching hierarchy of directories
    # should find 'data' directory
    max_levels = 3
    
    i = 0
    while i < max_levels:
        # 'data' directory is found
        if path / 'data' in path.iterdir():
            path = path / 'data'
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
        self.data_dir = find_data_dir(Path().cwd())
        self.data_file_name = 'FakeData.csv'
        self.data_path = self.data_dir / self.data_file_name        

        # formatting data
        self.column_names = ['Timestamp', 'Name', 'Email',
                        'Pref1', 'Pref2', 'Pref3', 'Pref4', 'Pref5',
                        'M_times', 'T_times', 'W_times', 'Th_times', 'F_times']

class AssignmentsConfig:
    def __init__(self):
        self.preprocess_config = PreprocessingConfig()
        
        self.group_sizes = list(range(3,5+1))


if __name__ == '__main__':
    config = PreprocessingConfig()

    print(f'Data directory: {config.data_dir}')


