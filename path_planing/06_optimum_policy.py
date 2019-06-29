#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ----------
# User Instructions:
# 
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
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
START = [0, 0]
GOAL = [len(WORLD)-1, len(WORLD[0])-1]

ACTION_COST = 1
ACTION_TYPE = [[-1, 0], # go up
               [ 0,-1], # go left
               [ 1, 0], # go down
               [ 0, 1]] # go right

ACTION_NAME = ['^', '<', 'v', '>']

def optimum_policy(world, goal, cost):
    value = [[99 for col in range(len(world[0]))] for row in range(len(world))]
    policy = [[' ' for col in range(len(world[0]))] for row in range(len(world))]

    change = True
    while change:
        change = False

        for x in range(len(world)):
            for y in range(len(world[0])):

                if x == goal[0] and y == goal[1]:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = "*"
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
                                policy[x][y] = ACTION_NAME[a]
                                change = True

    return value, policy

VALUE, POLICY = optimum_policy(WORLD, GOAL, ACTION_COST)
print("value:")
for row in VALUE:
    print(row)
print("policy:")
for row in POLICY:
    print(row)

