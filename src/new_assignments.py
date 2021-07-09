import math

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.bipartite.matching import minimum_weight_full_matching

from utils import configs
from preprocessing import preprocess


def write_assignment(assignments, lab_groups, file_name, write_score: bool=False, score: int=0):
    """Writes the given time/student configurations to a specified .txt file."""

    with open(file_name, "w") as f:
        if write_score:
            f.write(f"Unhappiness level: {score}\n")

        grouped_assignments = {lab_group.name: [] for lab_group in lab_groups}
        for key, val in assignments.items():
            key_split = str(key).split(' : ')
            if key_split[0] in grouped_assignments:
                grouped_assignments[key_split[0]].append(str(val))

        for lab_group_name, students in grouped_assignments.items():
            f.write(f'{lab_group_name}\n{"-" * len(lab_group_name)}\n')
            for student_name in students:
                f.write(f'{student_name}\n')
            f.write(f'\n' * 3)


def cost(student, lab_group):
    """Computes the inverse 'preference' of a lab group for a student.
    
    If a student prefers a lab group, the cost will be lower.
    If a student does not prefer a lab group, the cost will be higher.
    """

    return student.preferences.index(lab_group.name)


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

    # construct the nodes of the graph
    G = nx.Graph()
    X = [student.name for student in students]
    Y = [f'{lab_group.name} : {time}' for time in lab_group.good_times for lab_group in lab_groups]
    Y = [label + f'{num+1}' for label in Y for num in range(0, math.ceil(len(students) / len(lab_groups)))]
    # print(f'Students: {len(students)}\nLab Groups: {len(lab_groups)}\n{math.ceil(len(students) / len(lab_groups))}')
    # print(len(Y))
    G.add_nodes_from(X, bipartite=0)
    G.add_nodes_from(Y, bipartite=1)

    # construct the edges of the graph
    for lab_group in lab_groups:
        for time, compat_students in lab_group.good_times.items():
            for student in compat_students:
                G.add_edge(student.name, f'{lab_group.name} : {time}', weight=cost(student, lab_group))

    assignment = minimum_weight_full_matching(G, top_nodes=X)
    # for key, val in matching.items():
    #     print(key, val)

    # nx.draw(G, node_size=30/max(len(X), len(Y)), pos=nx.bipartite_layout(G, X))
    # plt.show()

    write_assignment(assignment, lab_groups, config.data_dir/'assignment.txt')

    return assignment


if __name__ == "__main__":
    cfg = configs.AssignmentsConfig()

    student_data, lab_group_data = preprocess(cfg)
    find_assignments(student_data, lab_group_data, cfg)

    with open(cfg.preprocess_config.data_dir/"finished.txt", "w") as finish_file:
        finish_file.write("Finished!")