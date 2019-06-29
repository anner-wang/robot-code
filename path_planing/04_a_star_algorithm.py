#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# -----------
# User Instructions:
#
# Modify the the search function so that it becomes
# an A* search algorithm as defined in the previous
# lectures.
#
# Your function should return the expanded grid
# which shows, for each element, the count when
# it was expanded or -1 if the element was never expanded.
# 
# If there is no path from init to goal,
# the function should return the string 'fail'
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

HEURISTIC = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]
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
    h = HEURISTIC[x][y]
    f = g + h
    
    open = [[f, g, h, x, y]]
    found = False
    resign = False
    count = 0

    while found is False and resign is False:
        if len(open) == 0:
            resign = True
            print("#### Search Failed ####")
        else:
            open.sort()
            # print("sort:", open)
            open.reverse()
            # print("reverse:", open)
            next = open.pop()
            # print("next:", next)
            
            x = next[3]
            y = next[4]
            g = next[1]
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
                            h2 = HEURISTIC[x2][y2]
                            f2 = g2 + h2
                            open.append([f2, g2, h2, x2, y2])
                            # print("append checked cell:", [f2, g2, h2, x2, y2])
                            closed[x2][y2] = 1
                            action[x2][y2] = i

    print("closed:")
    for i in range(len(closed)):
        print(closed[i])

    print("expand:")
    for i in range(len(expand)):
        print(expand[i])

    print("action:")
    for i in range(len(action)):
        print("[", end=" ")
        for j in range(len(action[0])):
            if action[i][j] != -1 :
                print(ACTION_NAME[action[i][j]], end = " ")
            else:
                print(action[i][j], end = " ")
        print("]")


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
