import os
from collections import OrderedDict

class AssignmentsConfig:
    def __init__(self):
        self.data_path = os.path.join('./data_f19.xlsx')

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
