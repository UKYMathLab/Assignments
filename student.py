class Student:
    def __init__(self):
        self.name = ''
        self.available_times = set()
        self.preferences = []
        self.is_assigned = False
        self.assignments = set()

    def assign(self, group_id: str):
        self.assignments.add(group_id)
        self.is_assigned = True
    def unassign(self, group_id: str):
        self.assignments.remove(group_id)
        self.is_assigned = False
