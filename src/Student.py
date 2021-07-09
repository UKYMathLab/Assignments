from typing import Set, List

class Student:
    def __init__(self, name: str='', email: str='', available_times: Set=set(), preferences: List=[]):
        self.name = str(name)
        self.email = str(email)

        self.available_times = available_times
        self.preferences = preferences
