class Student:
    def __init__(self, name: str='', email: str='', available_times: set=set(), preferences: list=[]):
        self.name = str(name)
        self.email = str(email)

        self.available_times = available_times
        self.preferences = preferences
