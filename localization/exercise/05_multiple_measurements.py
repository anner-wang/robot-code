#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Modify the code so that it updates the probability twice and gives
the posterior distribution after both measurements are incorporated.
Make sure that your code allows for any sequrence of measurement of
any length.
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
MEASUREMENTS = ['red', 'green']
PROB_HIT = 0.6
PROB_MISS = 0.2

###
# ADD YOUR CODE HERE
###

print(P)
