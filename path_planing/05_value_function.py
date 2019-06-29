#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------
"""

# WORLD = [[0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 0, 0, 0, 1, 0]]
WORLD = [[0, 0, 0, 0, 0, 0],
         [0, 0, 1, 1, 1, 1],
         [0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0]]

GOAL = [len(WORLD)-1, len(WORLD[0])-1]

ACTION_COST = 1
ACTION_TYPE = [[-1, 0], # go up
               [ 0,-1], # go left
               [ 1, 0], # go down
               [ 0, 1]] # go right

ACTION_NAME = ['^', '<', 'v', '>']

def compute_value(world, goal, cost):
    value = [[99 for col in range(len(world[0]))] for row in range(len(world))]
    change = True

    while change:
        change = False
        for x in range(len(world)):
            for y in range(len(world[0])):

                if x == goal[0] and y == goal[1]:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        change = True
                
                elif world[x][y] == 0:
                    for a in range(len(ACTION_TYPE)):
                        x2 = x + ACTION_TYPE[a][0]
                        y2 = y + ACTION_TYPE[a][1]
                        if x2 >= 0 and x2 < len(world) and \
                           y2 >= 0 and y2 < len(world[0]) and \
                           world[x2][y2] == 0:
                            v2 = value[x2][y2] + cost
                            if v2 < value[x][y]:
                                value[x][y] = v2
                                change = True

    return value

VALUE = compute_value(WORLD, GOAL, ACTION_COST)

print("value:")
for row in VALUE:
        print(row)
