# Assignments
The overarching goal is to be able to automatically assign teaching assistant (TA) positions to a set of graduate students for all classes under many constraints while maintaining a good score for "happiness". Some example constraints include time availability of the student, seniority of the student, or professor preferences for certain students. We will call this the TA assignment problem.

To tackle this problem, first we take a smaller problem of assigning undergraduate students to Math Lab groups given their preferences and available times. By solving this smaller problem with less constraints, we should be able to apply some of the same methods to the harder TA assignment problem. We will call this the Math Lab assignment problem.

# "Happiness"
One of the biggest challenges with solving assignment problems is how does one quantify the stability, or "happiness", of the matching. Some approaches tackle this by forming a list of the preferences and finding the index offset between the found matching and the index into the preference list, and then summing this for each student.

# Approaches
1. Brute force search the space of possible combinations of students, times, and preferences and find a combination that minimizes some "happiness" criteria. For small sets, this is computationally feasible.

# How to Run
1. Place the two CSV files in `./Assignments/data/raw_data/`.
2. In `./Assignments/src/utils/configs.py`, navigate to `class PreprocessingConfig`. From here, simply change the values of `self.student_data_subdir` and `self.lab_group_data_subdir` to `raw_data` (if this is not already done). Next change the values of `self.student_data_file_name` and `self.lab_group_data_file_name` to their respective file names. Save the file!
3. Navigate to `./Assignments/src/` and run the algorithm by executing `python assignments.py` in the command line.

