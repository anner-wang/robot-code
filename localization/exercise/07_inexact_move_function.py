#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Modify the move function to accommodate the added probabilities of
overshooting or undershooting the intented destination.
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

def move(probabilities, motion, prob_exact, prob_undershoot, prob_overshoot):
    """
    output the shifted probability distribution after moving
    """
    result = []
    ###
    # ADD YOUR CODE HERE
    ###
    return result


WORLD = ['green', 'red', 'red', 'green', 'green']
P = [0, 1, 0, 0, 0]
MEASUREMENTS = ['red', 'green']
PROB_HIT = 0.6
PROB_MISS = 0.2
PROB_EXACT = 0.8
PROB_OVERSHOOT = 0.1
PROB_UNDERSHOOT = 0.1

print(move(P, 1, PROB_EXACT, PROB_OVERSHOOT, PROB_UNDERSHOOT))
