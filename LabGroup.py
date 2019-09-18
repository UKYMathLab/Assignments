class LabGroup:
    def __init__(self, group_name: str, available_times: set):
        self.name = group_name

        self.available_times = available_times

        self.possible_group_members = []
        self.actual_group_members = []

        self.three_student_combos = []   # list of sets
        self.four_student_combos = []    # list of sets
        self.five_student_combos = []    # list of sets
