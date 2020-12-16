def compareSequences(sq1, sq2):
    if len(sq1) == 0 or len(sq2) == 0:
        return False
    if len(sq1) > len(sq2):
        parent = sq1.copy()
        child = sq2.copy()
    else:
        parent = sq2.copy()
        child = sq1.copy()
    indices = []
    for i in range(len(parent)):
        if child[0] == parent[i]:
            indices.append(i)
    for index in indices:
        is_found = True
        parent_index = index
        for item in child:
            if item != parent[parent_index]:
                is_found = False
            parent_index += 1
            if parent_index >= len(parent):
                parent_index = 0
        if is_found:
            return True
    return False


# Testing the function
'''
# Smaller set in larger
l1 = [2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635]
l2 = [7706, 7701, 5019, 8253]
print("This should be true: " + str(compareSequences(l2, l1)))
# Set not in same order
l1 = [2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635]
l2 = [7706, 7701, 5019, 2060, 6254]
print("This should be false: " + str(compareSequences(l2, l1)))
# Single value in set
l2 = [2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635]
l1 = [8635]
print("This should be true: " + str(compareSequences(l2, l1)))
# Same set
l1 = [2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635]
l2 = [2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635]
print("This should be true: " + str(compareSequences(l2, l1)))
# Same set but must loop to the beginning
l1 = [2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635]
l2 = [5019, 8253, 2060, 6254, 8635, 2267, 4654, 3637, 7706, 7701]
print("This should be true: " + str(compareSequences(l2, l1)))
# Each value is off by 1
l1 = [2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635]
l2 = [5018, 8252, 2059, 6253, 8634, 2266, 4653, 3636, 7705, 7700]
print("This should be false: " + str(compareSequences(l2, l1)))
l1 = [[2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635]]
l2 = []
print("This should be false: " + str(compareSequences(l2, l1)))
'''