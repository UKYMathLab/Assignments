# Assignments
The overarching goal is to be able to automatically assign teaching assistant (TA) positions to a set of graduate students for all classes under many constraints while maintaining a good score for "happiness". Some example constraints include time availability of the student, seniority of the student, or professor preferences for certain students. We will call this the TA assignment problem.

To tackle this problem, first we take a smaller problem of assigning undergraduate students to Math Lab groups given their preferences and available times. By solving this smaller problem with less constraints, we should be able to apply some of the same methods to the harder TA assignment problem. We will call this the Math Lab assignment problem.

# "Happiness"
One of the biggest challenges with solving assignment problems is how does one quantify the stability, or "happiness", of the matching. Some approaches tackle this by forming a list of the preferences and finding the index offset between the found matching and the index into the preference list, and then summing this for each student.

# Approaches
1. Brute force search the space of possible combinations of students, times, and preferences and find a combination that minimizes some "happiness" criteria. For small sets, this is computationally feasible.
