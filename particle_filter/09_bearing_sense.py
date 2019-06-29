#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# Write a function in the class Robot called sense() that takes
# self as input and returns a list, Z, of the four bearings to 
# the 4 different landmarks. you will have to use the robot's
# x and y position, as well as its orientation, to compute this.
"""
from math import sin, cos, pi, sqrt, exp, atan2
import random

LANDMARKS = [[100, 0],
             [0, 0],
             [0, 100],
             [100, 100]]
# world is NOT cyclic. Robot is allowed to travel "out of bounds"
WORLD_SIZE = 100

class Robot:
    """
    Robot class encapsulation
    """
    def __init__(self):
        """
        creates robot and initializes location/orientation
        """
        self.x = random.random() * WORLD_SIZE
        self.y = random.random() * WORLD_SIZE
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.bearing_noise = 0.0

    def set(self, new_x, new_y, new_orientation):
        """
        set a robot coordination
        """
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_b_noise):
        """
        makes it possible to change the noise parameters
        this is often useful in particle filters
        """
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.bearing_noise = float(new_b_noise)

    def sense(self, add_noise=1):
        """
        measuremnet the bearings of robot to each landmarks
        """
        z = []
        for i in range(len(LANDMARKS)):
            bearing = atan2(LANDMARKS[i][1] - self.y,
                            LANDMARKS[i][0] - self.x) - self.orientation
            if add_noise:
                bearing += random.gauss(0.0, self.bearing_noise)
            bearing %= 2 * pi
            z.append(bearing)
        return z

    def move(self, turn, forward):
        """
        move robot with turning and motion command
        """
        if forward < 0:
            raise ValueError('Robot cannot move backwards')

        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)

        # set particle
        result = Robot()
        result.set(x, y, orientation)
        result.set_noise(self.forward_noise, self.turn_noise, self.bearing_noise)
        return result

    def gaussian(self, mu, sigma, x):
        """
        calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        """
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurements):
        """
        calculates how likely a measurement should be
        """
        prob = 1.0
        for i in range(len(LANDMARKS)):
            bearing = atan2(LANDMARKS[i][1] - self.y,
                            LANDMARKS[i][0] - self.x) - self.orientation
            bearing %= 2 * pi

            prob *= self.gaussian(bearing, self.bearing_noise, measurements[i])
        return prob

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x)
        dy = (p[i].y - r.y)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))


###########################################

myrobot = Robot()

N = 1000
p = []
for i in range(N):
    r = Robot()
    r.set_noise(5.0, 0.1, 0.1)
    p.append(r)

print(eval(myrobot, p))

T = 8
for t in range(T):
    myrobot = myrobot.move(2. * pi / 10, 20)
    Z = myrobot.sense()

    p2 = []
    for i in range(N):
        p2.append(p[i].move(2. * pi / 10, 20))
    p = p2

    w = []
    for i in range(N):
        w.append(p[i].measurement_prob(Z))

    p3 = []
    index = int(random.random() * N)
    beta = 0
    max_w = max(w)
    for i in range(N):
        beta += random.random() * 2 * max_w
        while beta > w[index]:
            beta -= w[index]
            index = (index + 1) % N
        p3.append(p[index])
    p = p3

    # for i in range(N):
    #     print(p[i], w[i])

print(eval(myrobot, p))