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

def sense_2d(world, probabilities, measurement, prob_sensor):
    """
    output the normalized probability distribution of 2d-world
    """
    row_number = len(probabilities)
    col_number = len(probabilities[0])
    result = [[0.0 for col in range(col_number)] for row in range(row_number)]
    sum_of_prob = 0.0

    for i in range(row_number):
        for j in range(col_number):
            hit = (measurement == world[i][j])
            result[i][j] = probabilities[i][j] * (hit * prob_sensor + (1 - hit) * (1 - prob_sensor))
            sum_of_prob += result[i][j]

    for i in range(row_number):
        for j in range(col_number):
            result[i][j] /= sum_of_prob

    return result


def move_2d(probabilities, motion, prob_move):
    """
    output the shifted probability distribution after moving within 2d-world
    """
    row_number = len(probabilities)
    col_number = len(probabilities[0])
    result = [[0.0 for col in range(col_number)] for row in range(row_number)]
    for i in range(row_number):
        for j in range(col_number):
            result[i][j] = (prob_move * probabilities[(i - motion[0]) % row_number][(j - motion[1]) % col_number]) \
                            + ((1 - prob_move) * probabilities[i][j])
    return result

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

    for k in range(len(measurements)):
        result = move_2d(result, motions[k], prob_move)
        result = sense_2d(world, result, measurements[k], prob_sensor)

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


"""
# test 1
colors = [['G', 'G', 'G'],
          ['G', 'R', 'G'],
          ['G', 'G', 'G']]
measurements = ['R']
motions = [[0,0]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0]])

# test 2
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R']
motions = [[0,0]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.5, 0.5],
     [0.0, 0.0, 0.0]])

# test 3
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R']
motions = [[0,0]]
sensor_right = 0.8
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.06666666666, 0.06666666666, 0.06666666666],
     [0.06666666666, 0.26666666666, 0.26666666666],
     [0.06666666666, 0.06666666666, 0.06666666666]])

# test 4
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 0.8
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.03333333333, 0.03333333333, 0.03333333333],
     [0.13333333333, 0.13333333333, 0.53333333333],
     [0.03333333333, 0.03333333333, 0.03333333333]])

# test 5
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.0, 1.0],
     [0.0, 0.0, 0.0]])

# test 6
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 0.8
p_move = 0.5
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0289855072, 0.0289855072, 0.0289855072],
     [0.0724637681, 0.2898550724, 0.4637681159],
     [0.0289855072, 0.0289855072, 0.0289855072]])

# test 7
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 1.0
p_move = 0.5
p = localize(colors,measurements,motions,sensor_right,p_move)
correct_answer = (
    [[0.0, 0.0, 0.0],
     [0.0, 0.33333333, 0.66666666],
     [0.0, 0.0, 0.0]])
"""
