#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Modify the code below so that the function sense, which
takes p and Z as inputs, will output the NON-normalized
probability distribution, q, after multiplying the entries
in p by pHit or pMiss according to the color in the
corresponding cell in world.
"""

def sense(world, probabilities, measurement, prob_hit, prob_miss):
    """
    output the NON-normalized probability distribution of world
    """
    result = []
    ###
    # ADD YOUR CODE HERE
    ###
    return result

WORLD = ['green', 'red', 'red', 'green', 'green']
P = [0.2, 0.2, 0.2, 0.2, 0.2]
MEASUREMENT = 'red'
PROB_HIT = 0.6
PROB_MISS = 0.2

print(sense(WORLD, P, MEASUREMENT, PROB_HIT, PROB_MISS))
