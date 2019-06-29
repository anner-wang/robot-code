#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Modify the code below so that it normalizes the output for the function sense.
This means that the entries in result list should sum to 1.
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

WORLD = ['green', 'red', 'red', 'green', 'green']
P = [0.2, 0.2, 0.2, 0.2, 0.2]
MEASUREMENT = 'green'
PROB_HIT = 0.6
PROB_MISS = 0.2

print(sense(WORLD, P, MEASUREMENT, PROB_HIT, PROB_MISS))
