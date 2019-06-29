#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
The function localize takes the following arguments:
world:
       2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
measurements:
       list of measurements taken by the robot, each entry either 'R' or 'G'
motions:
       list of actions taken by the robot, each entry of the form [dy,dx],
       where dx refers to the change in the x-direction (positive meaning
       movement to the right) and dy refers to the change in the y-direction
       (positive meaning movement downward)
       NOTE: the *first* coordinate is change in y; the *second* coordinate is
             change in x
prob_sensor:
       float between 0 and 1, giving the probability that any given
       measurement is correct; the probability that the measurement is
       incorrect is 1-prob_sensor
prob_move:
       float between 0 and 1, giving the probability that any given movement
       command takes place; the probability that the movement command fails
       (and the robot remains still) is 1-prob_move; the robot will NOT overshoot
       its destination in this exercise
The function should RETURN (not just show or print) a 2D list (of the same
dimensions as world) that gives the probabilities that the robot occupies
each cell in the world.
Compute the probabilities by assuming the robot initially has a uniform
probability of being in any cell.
Also assume that at each step, the robot:
1) first makes a movement,
2) then takes a measurement.
Motion:
 [0,0] - stay
 [0,1] - right
 [0,-1] - left
 [1,0] - down
 [-1,0] - up
"""


def show(probability_2d):
    """
    print the probability list corresponding to the 2d-world
    """
    rows = ['[' + ', '.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in probability_2d]
    print('[' + ',\n '.join(rows) + ']')

def localize_2d(world, measurements, motions, prob_sensor, prob_move):
    """
    output the localization probability distribution with moving and sensing sequence
    """
    if len(measurements) != len(motions):
        raise ValueError("error in size of measurement/motion vector")

    # initializes matrix of probabilities to a uniform distribution over a grid of the same dimensions as world
    row_number = len(world)
    col_number = len(world[0])
    pinit = 1.0 / float(row_number) / float(col_number)
    result = [[pinit for col in range(col_number)] for row in range(row_number)]

    ###
    # << ADD YOUR CODE HERE >>
    ###

    return result


WORLD = [['R', 'G', 'G', 'R', 'R'],
         ['R', 'R', 'G', 'R', 'R'],
         ['R', 'R', 'G', 'G', 'R'],
         ['R', 'R', 'R', 'R', 'R']]
MOTIONS = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]
MEASUREMENTS = ['G', 'G', 'G', 'G', 'G']
PROB_SENSOR = 0.7
PROB_MOVE = 0.8
P = localize_2d(WORLD, MEASUREMENTS, MOTIONS, PROB_SENSOR, PROB_MOVE)
show(P)
