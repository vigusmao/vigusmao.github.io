from random import randint
from time import time



MAX_VALUE = 10**5


def intersection_n2(list1, list2):
    count = 0
    for element in list1:
        if element in list2:
            count += 1
    return count

def intersection_n(list1, list2):
    count = 0
    element_set = set()
    for element in list1:
        element_set.add(element)
    for candidate in list2:
        if candidate in element_set:
            count += 1
    return count

def create_list(size):
    tempset = set()
    while len(tempset) < size:
        tempset.add(randint(1, MAX_VALUE))
    return list(tempset)
       

def clock(method, arguments):
    start = time()
    result = method(*arguments)
    duration = time() - start
    print("\nResult = %d (%s) --- elapsed: %.6f ms" %
          (result, method.__name__, duration))


while True:
    N = eval(input(" Size: " ))
    list1 = create_list(N)
    list2 = create_list(N)
    clock(intersection_n2, (list1, list2))
    clock(intersection_n, (list1, list2))
    print()
    












