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

partitions(20)
