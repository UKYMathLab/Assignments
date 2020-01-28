# Assignments
The overarching goal is to be able to automatically assign teaching assistant (TA) positions to a set of graduate students for all classes under many constraints while maintaining a good score for "happiness". Some example constraints include time availability of the student, seniority of the student, or professor preferences for certain students. We will call this the TA assignment problem.

To tackle this problem, first we take a smaller problem of assigning undergraduate students to Math Lab groups given their preferences and available times. By solving this smaller problem with less constraints, we should be able to apply some of the same methods to the harder TA assignment problem. We will call this the Math Lab assignment problem.

# How to Run
1. Place the two CSV files anywhere in `/Assignments/data/`.
2. Change your current directory to `/Assignments/src/`.
3. From the command line, execute `python assignments.py` (include command line arguments to choose different options as shown in the example)

### Example
`python assignments.py --s_data="student_sample.csv" --lg_data="faculty_sample.csv" --file_format="S_2020" --min_size=3 --max_size=5
`.
* `--s_data` indicates to load student data from `student_sample.csv`
* `--lg_data` indicates to load faculty/lab group data from `faculty_sample.csv`
* `--file_format` determines how the CSV files are parsed. The CSV's from Fall 2019 should use `--file_format="F_2019"` and the most recent files should use `--file_format="S_2020"`.
* `--min_size` sets a lower bound for the size of a potential lab group.
* `--max_size` set an upper bound for the size of a potential lab group.

