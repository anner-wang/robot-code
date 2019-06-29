#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Program a function that returns a new probability distribution
which shifted to the right by specified steps. if U=0, the result should
be the same as P.
"""

def sense(world, probabilities, measurement, prob_hit, prob_miss):
    """
    output the normalized probability distribution of world
    """
    result = []
    for i in range(len(probabilities)):
        hit = (measurement == world[i])
        result.append(probabilities[i] * (hit * prob_hit + (1-hit) * prob_miss))
    result_sum = sum(result)
    for i in range(len(probabilities)):
        result[i] = result[i] / result_sum
    return result

def move(probabilities, motion):
    """
    output the shifted probability distribution after moving
    """
    result = []
    length = len(probabilities)
    for i in range(length):
        result.append(probabilities[(i - motion) % length])
    # position = motion % len(probabilities)
    # result = probabilities[-position:] + probabilities[:-position]
    return result

WORLD = ['green', 'red', 'red', 'green', 'green']
P = [1/9, 1/3, 1/3, 1/9, 1/9]
MEASUREMENTS = ['red', 'green']
PROB_HIT = 0.6
PROB_MISS = 0.2
print(move(P, 1))
