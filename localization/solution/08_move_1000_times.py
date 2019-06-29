#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Write code that moves 1000 times and then prints the
resulting probability distribution.
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
    length = len(probabilities)
    for i in range(length):
        prob = prob_exact * probabilities[(i - motion) % length]
        prob = prob + prob_overshoot * probabilities[(i - motion - 1) % length]
        prob = prob + prob_undershoot * probabilities[(i - motion + 1) % length]
        result.append(prob)
    return result

P = [0, 1, 0, 0, 0]
WORLD = ['green', 'red', 'red', 'green', 'green']
MEASUREMENTS = ['red', 'green']
PROB_HIT = 0.6
PROB_MISS = 0.2
PROB_EXACT = 0.8
PROB_OVERSHOOT = 0.1
PROB_UNDERSHOOT = 0.1

for step in range(1000):
    P = move(P, 1, PROB_EXACT, PROB_UNDERSHOOT, PROB_OVERSHOOT)

print(P)
