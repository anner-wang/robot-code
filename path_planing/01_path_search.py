#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# World format:
#   0 = Navigable space
#   1 = Occupied space
"""
# WORLD = [[0, 0, 1, 0, 0, 0],
#          [0, 0, 1, 0, 0, 0],
#          [0, 0, 1, 0, 1, 0],
#          [0, 0, 1, 1, 1, 0],
#          [0, 0, 1, 0, 1, 0]]
WORLD = [[0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
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
    
    x = start[0]
    y = start[1]
    g = 0
    
    open = [[g, x, y]]
    found = False
    resign = False
    
    print("initial open list:")
    for i in range(len(open)):
        print(open[i])
    print("----")

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
            
            if x == goal[0] and y == goal[1]:
                found = True
                print("#### Search Successful ####")
                print(next)
            else:
                for i in range(len(ACTION_TYPE)):
                    x2 = x + ACTION_TYPE[i][0]
                    y2 = y + ACTION_TYPE[i][1]
                    if x2 >= 0 and x2 < len(world) and y2 >= 0 and y2 < len(world[0]):
                        if closed[x2][y2] == 0 and world[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            print("append checked cell:", [g2, x2, y2])
                            closed[x2][y2] = 1
    
    path = open.sort()
    return path

search(WORLD, START, GOAL, ACTION_COST)