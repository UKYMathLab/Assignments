from collections import Counter
from typing import Set


class LabGroup:
    def __init__(self, group_name: str='', available_times: Set=set()):
        self.name = group_name

        self.available_times = available_times
        # dictionary of times (key) with compatible students as sets (value)
        self.good_times = dict()

        self.possible_members = set()
        self.actual_members = set()

    def __str__(self):
        return self.name

    def find_members(self, students):
        """Finds compatible students based on time."""

        for time in self.available_times:
            for student in students:
                # check if intersection is nonempty
                if time in student.available_times:
                    # check if key is already in dictionary
                    if time not in self.good_times:
                        self.good_times[time] = set()
                    self.good_times[time].add(student)
                    self.possible_members.add(student)
                # else discard
    
    def find_common_time(self):
        """Finds the time(s) that work best for the most students."""
        time_counts = Counter(time for student in self.actual_members for time in student.available_times)
        
        return time_counts.most_common(n=1)[0]