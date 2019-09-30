class LabGroup:
    def __init__(self, group_name: str, available_times: set):
        self.name = group_name

        self.available_times = available_times

        self.possible_group_members = []
        self.actual_group_members = []

        self.possible_groups = {3: [], 4: [], 5: []}
