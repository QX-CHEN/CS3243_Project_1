from random import shuffle
from CS3243_P1_01_1 import Puzzle, Node
from time import time

def test():
    dimension = eval(input("Enter dimension:"))
    n = eval(input("Enter number of times:"))
    goal_state = convert_list_to_2d(dimension, [e for e in range(1, dimension*dimension)] + [0])
    print(goal_state)
    for i in range(n):
        start = time()
        curr = generate_puzzle(dimension)
        print(curr)
        puzzle = Puzzle(curr, goal_state)
        ans = puzzle.solve()
        end = time()
        print(ans)
        print(end - start)
    # print_2d_lst(generate_puzzle(5))
    return

def generate_puzzle(dimension):
    lst = [e for e in range(dimension*dimension)]
    shuffle(lst)
    return convert_list_to_2d(dimension, lst)

def convert_list_to_2d(dimension, lst):
    res = []
    for i in range(0, len(lst), dimension):
        res.append(lst[i:i+dimension])
    return res

def print_2d_lst(two_d_lst):
    print('\n'.join(str(lst) for lst in two_d_lst))

test()
