# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
from heapq import heappush, heappop, heapify
# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.dimension = len(init_state)
        # you may add more attributes if you think is useful
        self.init_state = self.convert_to_tuple(init_state)
        self.goal_state = self.convert_to_tuple(goal_state)
        # all possible actions
        self.actions = ["LEFT", "RIGHT", "UP", "DOWN"]
        # Attributes added
        self.init_zero_position = self.zero_position(init_state)

    def solve(self):
        # implement your search algorithm here
        return self.A_STAR()

    def convert_to_tuple(self, two_dim_list):
        res = tuple()
        for lst in two_dim_list:
            res += tuple(lst)
        return res

    def A_STAR(self):
        node = Node(self.init_state, self.dimension, self.init_zero_position)
        if not self.is_solvable(node):
            return ["UNSOLVABLE"]
        frontier = [node]
        heapify(frontier)
        explored = set()
        while frontier:
            node = heappop(frontier)
            if node.state in explored:
                continue
            if self.goal_test(node.state):
                return node.solution
            explored.add(node.state)
            for act in node.possible_actions:
                child = self.child_node(node, act)
                if (child.state not in explored):
                    heappush(frontier, child)

    def goal_test(self, state):
        return self.goal_state == state

    def child_node(self, node, act):
        ''' return a node with 
            updated state, path_cost and solution '''

        new_state = node.state
        new_solution = node.solution[:]

        if act == "LEFT":
            new_solution.append("LEFT")
            new_zero_position = node.zero_position + 1
        elif act == "RIGHT":
            new_solution.append("RIGHT")
            new_zero_position = node.zero_position - 1
        elif act == "UP":
            new_solution.append("UP")
            new_zero_position = node.zero_position + self.dimension
        else:   # DOWN
            new_solution.append("DOWN")
            new_zero_position = node.zero_position - self.dimension
        
        # creating new state by tuple concatenation
        temp = node.state[new_zero_position]
        if new_zero_position < node.zero_position:
            new_state = node.state[:new_zero_position] + (0,) + node.state[new_zero_position + 1:node.zero_position] \
                        + (temp,) + node.state[node.zero_position + 1:]
        else:
            new_state = node.state[:node.zero_position] + (temp,) + node.state[node.zero_position + 1:new_zero_position] \
                        + (0,) + node.state[new_zero_position + 1:]

        return Node(new_state, self.dimension, new_zero_position, node.path_cost + 1, new_solution)
    
    def zero_position(self, state):
        ''' input a state so that it might be use to determine
            zero position for all state
            return an index '''
        count = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] == 0:
                    return count
                count += 1
    
    def inversion(self, state):
        count = 0
        for i in range(len(state) - 1, 0, -1):
            if state[i] == 0:
                continue
            for j in range(i - 1, -1, -1):
                if state[j] == 0:
                    continue
                if state[j] > state[i]:
                    count += 1
        return count

    def is_solvable(self, node):
        if len(node.state) % 2:   # n is odd
            return False if self.inversion(node.state) % 2 else True 
        else:
            return  (self.inversion(node.state) + node.zero_position // self.dimension) % 2


class Node(object):
    def __init__(self, state, dimension, zero_position, path_cost = 0, solution = []):
        self.state = state
        self.dimension = dimension
        self.path_cost = path_cost      # g()
        self.solution = solution
        self.zero_position = zero_position
        self.possible_actions = self.filter_actions(["LEFT", "RIGHT", "UP", "DOWN"])
        self.f_value = self.f()

    def __eq__(self, f_value):
        return self.f_value == f_value

    def __lt__(self, f_value):
        return self.f_value < f_value

    def __gt__(self, f_value):
        return self.f_value > f_value

    def f(self):
        ''' evaluation function '''
        return self.path_cost + self.h()    # g() + h()
    
    def h(self):
        ''' heuristic function '''
        return self.manhattan_distance()
    
    def manhattan_distance(self):
        distance = 0
        for i in range(len(self.state)):
            if not self.state[i]:   # zero entry
                continue
            else:
                right_position = self.state[i] - 1 
                curr_row, curr_col = i // self.dimension, i % self.dimension
                right_row, right_col = right_position // self.dimension, right_position % self.dimension
                distance += (abs(curr_row - right_row) + abs(curr_col - right_col))
        return distance

    def filter_actions(self, possible_actions):
        ''' Filter impossible actions based on 
            zero_position of current state '''
        if self.zero_position < self.dimension:  # 0 at the top row
            possible_actions.remove("DOWN")
        elif self.zero_position >= self.dimension * (self.dimension - 1):    # 0 at bottum row
            possible_actions.remove("UP")
        if self.zero_position % self.dimension == 0:  # 0 at the leftmost col.
            possible_actions.remove("RIGHT")
        elif (self.zero_position + 1) % self.dimension == 0:    # 0 at rightmost col.
            possible_actions.remove("LEFT")
        return possible_actions


if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







