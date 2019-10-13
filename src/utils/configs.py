import os
from pathlib import Path
from collections import OrderedDict

class AssignmentsConfig:
    def __init__(self):
        self.data_path = os.path.join('./data/data_f19.xlsx')

        self.time_encodings = OrderedDict({'9:00-9:30' : 0,
                                          '9:30-10:00' : 1,
                                          '10:00-10:30' : 2,
                                          '10:30-11:00' : 3,
                                          '11:00-11:30' : 4,
                                          '11:30-12:00' : 5,
                                          '12:00-12:30' : 6,
                                          '12:30-1:00' : 7,
                                          '1:00-1:30' : 8,
                                          '1:30-2:00' : 9,
                                          '2:00-2:30' : 10,
                                          '2:30-3:00' : 11,
                                          '3:00-3:30' : 12,
                                          '3:30-4:00' : 13,
                                          '4:00-4:30' : 14,
                                          '4:30-5:00' : 15 })
        self.group_encodings = OrderedDict({'A' : 1,
                                           'B' : 2,
                                           'C' : 3,
                                           'D' : 4,
                                           'E' : 5 })
        self.column_names = ['Name', *[*self.time_encodings], 'pref1', 'pref2', 'pref3', 'pref4']

    
def find_data_dir(path: Path):
    # find data directory by searching hierarchy of directories
    # should find 'data' directory
    par = path.parent
    max_tries = 3
    
    i = 0
    while i < max_tries:
        if par / 'data' in par.iterdir():
            path = par / 'data'
            i = max_tries + 1   # condition found, break out of while
        else:
            i += 1
            par = par.parent    # try again, but one directory up
            
        if i == max_tries:
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
                        'First', 'Second', 'Third', 'Fourth', 'Fifth',
                        'M_times', 'T_times', 'W_times', 'Th_times', 'F_times']
        
if __name__ == '__main__':
    config = PreprocessingConfig()

    print(f'Data directory: {config.data_dir}')


