#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Write code that outputs p after multiplying each entry by pHit or pMiss
at the appropriate places. Remember that the red cells 1 and 2 are hits
and the other green cells are misses.
"""

P = [0.2, 0.2, 0.2, 0.2, 0.2]
PROB_HIT = 0.6
PROB_MISS = 0.2

P[0] = P[0] * PROB_MISS
P[1] = P[1] * PROB_HIT
P[2] = P[2] * PROB_HIT
P[3] = P[3] * PROB_MISS
P[4] = P[4] * PROB_MISS

print("probability vectors:")
print(P)
print("sum of probability:")
print(sum(P))
