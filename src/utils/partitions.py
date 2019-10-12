def partitions(numberPeople, ):

    possiblePartitions = []

    for i in [3,4,5]:
        for j in [3,4,5]:
            for k in [3,4,5]:
                for l in [3,4,5]:
                    for n in [3,4,5]:
                        if i+j+k+l+n == numberPeople:
                            possiblePartitions.append([i,j,k,l,n])

    print(len(possiblePartitions), possiblePartitions)

# assume there is a list of LabGroup objects called *lab_groups*
good_partitions = []

for partition in possiblePartitions:
    # check if any groups are possible
    # if partition is valid, append to master list
    master_okay_group = True

    for i, group_size in enumerate(partition):
        if i == 3:
            if not(lab_groups[i].three_student_combos):
                master_okay_group = False
        elif i == 4:
            if not(lab_groups[i].four_student_combos):
                master_okay_group = False
        elif i == 5:
            if not(lab_groups[i].five_student_groups):
                master_okay_group = False

    if master_okay_group:
        good_partitions.append(partition)

# add all good combinations of lab groups
good_lab_group_combos = []
for partition in good_partitions:
    for combo1 in lab_groups[0]:
        for combo2 in lab_groups[1]:
            for combo3 in lab_groups[2]:
                for combo4 in lab_groups[3]:
                    for combo5 in lab_groups[4]:
                        good_lab_groups_combos.append([combo1, combo2, combo3, combo4, combo5])






partitions(20)
