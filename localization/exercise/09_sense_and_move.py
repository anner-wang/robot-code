#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Given the list motions=[1,1] which means the robot moves right and then
right again, compute the posterior distribution if the robot first senses
red, then moves right one, then senses green, then moves right again,
starting with a uniform prior distribution.
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


def localize(world, probabilities, measurements, motions, prob_hit, prob_miss, prob_exact, prob_undershoot, prob_overshoot):
    """
    output the localization probability distribution with moving and sensing sequence
    """
    if len(measurements) != len(motions):
        raise ValueError("error in size of measurement/motion vector")

    ###
    # << ADD YOUR CODE HERE >>
    ###

    return probabilities


WORLD = ['green', 'red', 'red', 'green', 'green']
P = [0.2, 0.2, 0.2, 0.2, 0.2]
MOTIONS = [1, 1]
MEASUREMENTS = ['red', 'green']
PROB_HIT = 0.6
PROB_MISS = 0.2
PROB_EXACT = 0.8
PROB_OVERSHOOT = 0.1
PROB_UNDERSHOOT = 0.1

P = localize(WORLD, P, MEASUREMENTS, MOTIONS, PROB_HIT, PROB_MISS, PROB_EXACT, PROB_UNDERSHOOT, PROB_OVERSHOOT)
print(P)
