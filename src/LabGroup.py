class LabGroup:
    def __init__(self, group_name: str, available_times: set):
        self.name = group_name

        self.available_times = available_times
        # dictionary of times (key) with compatible students as sets (value)
        self.good_times = dict()

        self.possible_group_members = []
        self.actual_group_members = []

        self.possible_groups = {3: [], 4: [], 5: []}

    def find_members(self, students):
        r"""Finds compatible students based on time."""

        for time in self.available_times:
            for student in students:
                # check if intersection is nonempty
                if len(self.available_times.intersect(student.available_times)) > 0:
                    self.good_times[time].add(student)
                # else discard

