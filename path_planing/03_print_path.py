#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. Note that the 'v' should be 
# lowercase. '*' should mark the goal cell.
#
# You may assume that all test cases for this function
# will have a path from init to goal.
# ----------
"""
# WORLD = [[0, 0, 1, 0, 0, 0],
#          [0, 0, 1, 0, 0, 0],
#          [0, 0, 1, 0, 1, 0],
#          [0, 0, 1, 1, 1, 0],
#          [0, 0, 1, 0, 1, 0]]
# WORLD = [[0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 0, 0, 0, 1, 0]]
# WORLD = [[0, 0, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 0, 0],
#          [0, 1, 0, 0, 1, 0]]
WORLD = [[0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 1, 0]]

START = [0, 0]
GOAL = [len(WORLD)-1, len(WORLD[0])-1]

ACTION_COST = 1
ACTION_TYPE = [[-1, 0], # go up
               [ 0,-1], # go left
               [ 1, 0], # go down
               [ 0, 1]] # go right

ACTION_NAME = ['^', '<', 'v', '>']

def search(world,start,goal,cost):
    closed = [[0 for col in range(len(world[0]))] for row in range(len(world))]
    closed[start[0]][start[1]] = 1
    expand = [[-1 for col in range(len(world[0]))] for row in range(len(world))]
    action = [[-1 for col in range(len(world[0]))] for row in range(len(world))]
    path = [[' ' for col in range(len(world[0]))] for row in range(len(world))]

    
    x = start[0]
    y = start[1]
    g = 0
    
    open = [[g, x, y]]
    found = False
    resign = False
    count = 0

    while found is False and resign is False:
        if len(open) == 0:
            resign = True
            print("#### Search Failed ####")
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            
            x = next[1]
            y = next[2]
            g = next[0]

            expand[x][y] = count
            count += 1
            
            if x == goal[0] and y == goal[1]:
                found = True
                print("#### Search Successful ####")
            else:
                for i in range(len(ACTION_TYPE)):
                    x2 = x + ACTION_TYPE[i][0]
                    y2 = y + ACTION_TYPE[i][1]
                    if x2 >= 0 and x2 < len(world) and y2 >= 0 and y2 < len(world[0]):
                        if closed[x2][y2] == 0 and world[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1
                            action[x2][y2] = i
    
    print("closed:")
    for i in range(len(closed)):
        print(closed[i])

    print("expand:")
    for i in range(len(expand)):
        print(expand[i])

    if found is True:
        print("path:")
        x = goal[0]
        y = goal[1]
        path[x][y] = '*'
        while x != start[0] or y != start[1]:
            x2 = x - ACTION_TYPE[action[x][y]][0]            
            y2 = y - ACTION_TYPE[action[x][y]][1]
            path[x2][y2] = ACTION_NAME[action[x][y]]
            x = x2
            y = y2

        for i in range(len(path)):
            print(path[i])

    return path

search(WORLD, START, GOAL, ACTION_COST)
