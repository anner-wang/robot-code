#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Now we want to simulate robot motion with our particles.
Each particle should turn by 0.1 and then move by 5. 
Don't modify the code below. Please enter your code at the bottom.
"""
from math import sin, cos, pi, sqrt, exp
import random

LANDMARKS = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
WORLD_SIZE = 100.0

class Robot:
    """
    Robot class encapsulation
    """
    def __init__(self):
        self.x = random.random() * WORLD_SIZE
        self.y = random.random() * WORLD_SIZE
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_orientation):
        """
        set robot position
        """
        if new_x < 0 or new_x >= WORLD_SIZE:
            raise ValueError('X coordinate out of bound')
        if new_y < 0 or new_y >= WORLD_SIZE:
            raise ValueError('Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        """
        makes it possible to change the noise parameters
        this is often useful in particle filters
        """
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def sense(self):
        """
        measuremnet the distances of robot to each landmarks with random sense noise
        """
        Z = []
        for i in range(len(LANDMARKS)):
            dist = sqrt((self.x - LANDMARKS[i][0]) ** 2 + (self.y - LANDMARKS[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def move(self, turn, forward):
        """
        move robot with turning and motion command
        """
        if forward < 0:
            raise ValueError('Robot cant move backwards')

        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= WORLD_SIZE    # cyclic truncate
        y %= WORLD_SIZE

        # set particle
        result = Robot()
        result.set(x, y, orientation)
        result.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return result

    def gaussian(self, mu, sigma, x):
        """
        calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        """
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):
        """
        calculates how likely a measurement should be
        """
        prob = 1.0
        for i in range(len(LANDMARKS)):
            dist = sqrt((self.x - LANDMARKS[i][0]) ** 2 + (self.y - LANDMARKS[i][1]) ** 2)
            prob *= self.gaussian(dist, self.sense_noise, measurement[i])
        return prob

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (WORLD_SIZE/2.0)) % WORLD_SIZE - (WORLD_SIZE/2.0)
        dy = (p[i].y - r.y + (WORLD_SIZE/2.0)) % WORLD_SIZE - (WORLD_SIZE/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))



####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####

N = 1000
p = []
for i in range(N):
    r = Robot()
    p.append(r)

p2 = []
for i in range(N):
    p2.append(p[i].move(0.1, 5.0))
p = p2
print(p2)
