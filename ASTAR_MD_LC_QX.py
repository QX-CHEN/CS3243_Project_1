# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
from collections import deque
from time import time
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

    # you may add more functions if you think is useful
    # def BFS(self):
    #     node = Node(self.init_state, self.dimension, self.init_zero_position)
    #     if not self.is_solvable(node):
    #         return ["UNSOLVABLE"]
    #     if self.goal_test(node.state):
    #         return node.solution
    #     frontier = deque([node])  # queue (insert left, pop right)
    #     explored = set()
    #     while frontier:
    #         node = frontier.pop()
    #         explored.add(node.state)
    #         for act in node.possible_actions:
    #             # print(act)
    #             child = self.child_node(node, act)
    #             if (child.state not in explored):
    #                 explored.add(child.state)
    #                 if self.goal_test(child.state):
    #                     # print(child.path_cost)
    #                     return child.solution
    #                 frontier.appendleft(child)
    #     return ["UNSOLVABLE"]   # return failure

    def A_STAR(self):
        node = Node(self.init_state, self.dimension, self.init_zero_position)
        if not self.is_solvable(node):
            return ["UNSOLVABLE"]
        frontier = [node]
        heapify(frontier)
        explored = set()
        # print(frontier)
        while frontier:
            # print(frontier)
            node = heappop(frontier)
            if node.state in explored:
                continue
            if self.goal_test(node.state):
                # print(node.state)
                return node.solution
            explored.add(node.state)
            for act in node.possible_actions:
                # print(act)
                child = self.child_node(node, act)
                if (child.state not in explored):
                    heappush(frontier, child)
        return ["FALSE"]   # return failure

    def goal_test(self, state):
        return self.goal_state == state

    def child_node(self, node, act):
        ''' return a node with 
            updated state, path_cost and solution '''

        new_state = node.state
        new_solution = node.solution[:]
        # print(new_state)
        # print(node.zero_position)
        # print(act)
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
        
        # print(new_zero_position)
        temp = node.state[new_zero_position]
        if new_zero_position < node.zero_position:
            new_state = node.state[:new_zero_position] + (0,) + node.state[new_zero_position + 1:node.zero_position] \
             + (temp,) + node.state[node.zero_position + 1:]
        else:
            new_state = node.state[:node.zero_position] + (temp,) + node.state[node.zero_position + 1:new_zero_position] \
             + (0,) + node.state[new_zero_position + 1:]
        # print(new_state)
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
        # print(count)
        return count

    def is_solvable(self, node):
        if len(node.state) % 2:   # n is odd
            # print(self.inversion(node.state))
            return False if self.inversion(node.state) % 2 else True 
        else:
            # print(self.inversion(node.state))
            # print(node.zero_position[0])
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
        return self.new_ver()
    
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

    def manhattan_distance_with_linear_conflict(self):
        score = 0
        for i in range(len(self.state)):
            if not self.state[i]:   # zero entry
                continue
            else:
                # Mamhattan distance
                right_position = self.state[i] - 1 
                curr_row, curr_col = i // self.dimension, i % self.dimension
                right_row, right_col = right_position // self.dimension, right_position % self.dimension
                # Swaping adjacent tiles gives right position
                conflict = 0
                if (i + 1) % self.dimension: # Exception last col
                    if self.state[i] == (i + 2) and self.state[i + 1] == (i + 1):
                        conflict += 1
                if i < self.dimension * (self.dimension - 1): # Except last row
                    if self.state[i] == (i + 1 + self.dimension) and self.state[i + self.dimension] == (i + 1):
                        conflict += 1
                score += (abs(curr_row - right_row) + abs(curr_col - right_col) + 2 * conflict)
        return score

    def new_ver(self):
        score = 0
        for i in range(len(self.state)):
            if not self.state[i]:   # zero entry
                continue
            else:
                # Mamhattan distance
                right_position = self.state[i] - 1 
                curr_row, curr_col = i // self.dimension, i % self.dimension
                right_row, right_col = right_position // self.dimension, right_position % self.dimension
                # Linear conflict
                conflict = 0

                # Ver3 Complete LC : O(n^2) where n is the dimension
                if (i + 1) % self.dimension: # Exception last col
                    if curr_row == right_row:
                        conflict += sum(map(lambda x : self.state[i] > x and x != 0 and (x - 1) // self.dimension == right_row, \
                                    self.state[i + 1 : curr_row * self.dimension + self.dimension]))
                if i < self.dimension * (self.dimension - 1): # Except last row
                    if curr_col == right_col:
                        conflict += sum(map(lambda x : self.state[i] > self.state[x] and \
                                    self.state[x] != 0 and (self.state[x] - 1) % self.dimension == right_col, \
                                    range(i + self.dimension, self.dimension * (self.dimension - 1) + curr_col + 1, self.dimension)))

                # Ver2 Incomplete LC stronger than Ver1 : O(1)
                # curr = self.state[i]
                # if (i + 1) % self.dimension: # Exception last col
                #     right = self.state[i + 1]
                #     if curr_row == right_row and curr > right and right != 0 and (right - 1) // self.dimension == right_row:
                #         conflict += 1
                # if i < self.dimension * (self.dimension - 1): # Except last row
                #     down = self.state[i + self.dimension]
                #     if curr_col == right_col and curr > down and down != 0 and down % self.dimension == right_col:
                #         conflict += 1

                # Ver1 Incomplete LC : O(1)
                # if (i + 1) % self.dimension: # Exception last col
                #     if self.state[i] == (i + 2) and self.state[i + 1] == (i + 1): 
                #     # right value for curr_pos = i + 1 + 1, next_pos = i + 1 + 1 - 1 = i + 1
                #         conflict += 1
                # if i < self.dimension * (self.dimension - 1): # Except last row
                #     if self.state[i] == (i + self.dimension + 1) and self.state[i + self.dimension] == (i + 1):
                #     # right value for curr_pos = i + dimension + 1, next_pos = i + dimension + 1 - dimension = i + 1
                #         conflict += 1
    
                # conflict += sum(map(lambda x :curr_row == right_row and self.state[i] < self.state[x] and i > x and self.state[x] != 0 and (self.state[x] - 1) // self.dimension == right_row, \
                #             range(curr_row * self.dimension, curr_row * self.dimension + self.dimension)))

                # conflict += sum(map(lambda x : curr_col == right_col and self.state[i] < self.state[x] and i > x and \
                #             self.state[x] != 0 and (self.state[x] - 1) % self.dimension == curr_col, \
                #             range(curr_col, self.dimension * (self.dimension - 1) + curr_col + 1, self.dimension)))

                score += (abs(curr_row - right_row) + abs(curr_col - right_col) + 2 * conflict)

        return score

    # def new_ver(self):
    #     score = 0
    #     conflict = 0
    #     for i in range(len(self.state)):
    #         if not self.state[i]:   # zero entry
    #             continue
    #         else:
    #             # Mamhattan distance
    #             right_position = self.state[i] - 1 
    #             curr_row, curr_col = i // self.dimension, i % self.dimension
    #             right_row, right_col = right_position // self.dimension, right_position % self.dimension
    #             # Linear conflict

    #             conflict += sum(map(lambda x :curr_row == right_row and self.state[i] < self.state[x] and i > x and self.state[x] != 0 and (self.state[x] - 1) // self.dimension == right_row, \
    #                         range(curr_row * self.dimension, curr_row * self.dimension + self.dimension)))

    #             conflict += sum(map(lambda x : curr_col == right_col and self.state[i] < self.state[x] and i > x and \
    #                         self.state[x] != 0 and (self.state[x] - 1) % self.dimension == curr_col, \
    #                         range(curr_col, self.dimension * (self.dimension - 1) + curr_col + 1, self.dimension)))

    #             score += (abs(curr_row - right_row) + abs(curr_col - right_col))
    #     score += 2 * conflict
    #     return score
        
    def h1(self):   # misplaced tiles
        count = 0
        for i in range(len(self.state)):
            if not self.state[i]:   # zero entry
                continue
            else:
                if (self.state[i] - 1) != i:
                    count += 1
        return count

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

    # Instantiate a 2D list of(self.dimension) n x n
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

    # Added to measure time
    total_time = 0
    for i in range(50):
        puzzle = Puzzle(init_state, goal_state)
        start = time()
        ans = puzzle.solve()
        end = time()
        total_time += end - start
    with open(sys.argv[2], 'a') as f:   # change from append mode to overwrite
        for answer in ans:
            f.write(answer+'\n')
        f.write("average time taken : " + str(total_time/50) + "\n")
        f.write("steps taken : " + str(len(ans)) + "\n")
        f.write("------------------------------------\n")







