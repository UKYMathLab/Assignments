import numpy as np
from scipy.optimize import linear_sum_assignment

from utils import configs
from preprocessing import preprocess


def write_assignment(lab_groups, file_name, write_score: bool=False, score: int=0):
    """Writes the given time/student configurations to a specified .txt file."""

    with open(file_name, 'w') as f:
        if write_score:
            f.write(f'Unhappiness level: {score}\n')

        for lab_group in lab_groups:
            f.write(f'{lab_group}\n{"-" * len(lab_group.name)}\n' + '\n'.join(student.name for student in lab_group.actual_members) + '\n'*3)


def compute_cost(student, lab_group) -> int:
    """Computes the inverse 'preference' of a lab group for a student.
    
    If a student prefers a lab group, the cost will be lower.
    If a student does not prefer a lab group, the cost will be higher.
    If a student cannot be assigned to a lab group, the cost will be infinity.

    Parameters
    ----------
    student : Student
        A student.
    lab_group : LabGroup.
        A lab group.

    Returns
    -------
    The cost of assigning the student to the lab group, an int.
    """
    return student.preferences.index(lab_group.name) if student in lab_group.possible_members else np.inf


def construct_cost_matrix(students, lab_groups, group_size: int=4):
    """Constructs the cost matrix associated to assigning students to lab groups.
    
    Parameters
    ----------
    students : List[Student]
        List of students.
    lab_groups : List[LabGroup]
        List of lab groups.
    group_size : int
        The number of members a lab group should have.

    Returns
    -------
    cost_matrix : np.ndarray
        THe cost matrix associated to assigning students to lab groups.
    """
    cost_matrix = np.empty((len(students), len(lab_groups)*group_size))
    for i, student in enumerate(students):
        for j, lab_group in enumerate(lab_groups):
            cost_matrix[i, group_size*j:group_size*j+group_size] = compute_cost(student, lab_group)

    return cost_matrix


def find_assignments(students, lab_groups, config):
    """Find the minimum-cost matching between students and lab groups.
    
    We can represent the assignment as a minimum-cost matching in the bipartite
    graph formed between sets X and Y, where X consists of students and Y consists
    of lab groups. Note that there might be multiple nodes shared by a single lab 
    group since the nodes will also contain a meeting time in their name.

    An edge is formed between a student and a (lab group, time) node iff the student
    can meet at that time. The edge weights are determined by a cost function so
    that preferences can help determine better assignments, e.g. weigh lab group
    assignment over a meeting time.
    """
    # match students with lab group times for each lab group
    for lab_group in lab_groups:
        lab_group.find_members(students)

    # find assignment via cost matrix
    cost_matrix = construct_cost_matrix(students, lab_groups, group_size=config.group_size)
    student_indices, lab_group_indices = linear_sum_assignment(cost_matrix)
    lab_group_indices = list(map(lambda x: x // config.group_size, lab_group_indices))

    # add students to their assigned lab groups
    for student_assignment, student in zip(lab_group_indices, students):
        lab_groups[student_assignment].actual_members.add(student)
    write_assignment(lab_groups, config.data_dir/'assignment.txt')


def main():
    config = configs.AssignmentsConfig()

    students, lab_groups = preprocess(config)
    find_assignments(students, lab_groups, config)

    with open(config.preprocess_config.data_dir/'finished.txt', 'w') as finish_file:
        finish_file.write('Finished!')


if __name__ == "__main__":
    main()