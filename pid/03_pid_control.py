#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# User Instructions
#
# Implement a P controller by running 100 iterations
# of robot motion. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau_p * CTE - tau_d * diff_CTE - tau_i * int_CTE
#
# where the integrated crosstrack error (int_CTE) is
# the sum of all the previous crosstrack errors.
# This term works to cancel out steering drift.
#
# Only modify code at the bottom! Look for the TODO.
"""
 
import random
import numpy as np
import matplotlib.pyplot as plt

class Robot(object):
    def __init__(self, length=20.0):
        """
        Creates robot and initializes location/orientation to 0, 0, 0.
        """
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation):
        """
        Sets a robot coordinate.
        """
        self.x = x
        self.y = y
        self.orientation = orientation % (2.0 * np.pi)

    def set_noise(self, steering_noise, distance_noise):
        """
        Sets the noise parameters.
        """
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

    def set_steering_drift(self, drift):
        """
        Sets the systematical steering drift parameter
        """
        self.steering_drift = drift

    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        """
        steering = front wheel steering angle, limited by max_steering_angle
        distance = total distance driven, most be non-negative
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = np.tan(steering2) * distance2 / self.length

        if abs(turn) < tolerance:
            # approximate by straight line motion
            self.x += distance2 * np.cos(self.orientation)
            self.y += distance2 * np.sin(self.orientation)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.orientation) * radius)
            self.y = cy - (np.cos(self.orientation) * radius)

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.orientation)

############## ADD / MODIFY CODE BELOW ####################
# ------------------------------------------------------------------------
#
# run - does a single control run

def run_p(robot, tau, n=500, speed=1.0):
    """
    P controller
    """
    x_trajectory = []
    y_trajectory = []
    for i in range(n):
        cte = robot.y
        steer = -tau * cte
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
        print(robot, steer)
    return x_trajectory, y_trajectory

def run_pd(robot, tau_p, tau_d, n=500, speed=1.0):
    """
    P-D controller
    """
    x_trajectory = []
    y_trajectory = []
    previous_cte = robot.y
    for i in range(n):
        cte = robot.y
        steer = -tau_p * cte - tau_d * (cte - previous_cte)
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
        previous_cte = cte
        print(robot, steer)
    return x_trajectory, y_trajectory
    
def run_pid(robot, tau_p, tau_d, tau_i, n=500, speed=1.0):
    """
    P-I-D controller
    """
    x_trajectory = []
    y_trajectory = []
    previous_cte = robot.y
    integral_cte = 0

    for i in range(n):
        cte = robot.y
        diff_cte = cte - previous_cte
        integral_cte += cte
        previous_cte = cte

        steer = -tau_p * cte - tau_d * (diff_cte) - tau_i * integral_cte
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
        print(robot, steer)

    return x_trajectory, y_trajectory

robot1 = Robot()
robot1.set(0, 1, 0)
robot1.set_steering_drift(10 / 180 * np.pi)
x_trajectory1, y_trajectory1 = run_pid(robot1, 0.1, 3.0, 0.004)
n1 = len(x_trajectory1)


robot2 = Robot()
robot2.set(0, 1, 0)
robot2.set_steering_drift(10 / 180 * np.pi)
# x_trajectory2, y_trajectory2 = run_pid(robot2, 0.3, 5.0, 0.04)
x_trajectory2, y_trajectory2 = run_pid(robot2, 7.0, 15.0, 0.5)
n2 = len(x_trajectory2)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
ax1.plot(x_trajectory1, y_trajectory1, 'g', label='P controller')
ax1.plot(x_trajectory1, np.zeros(n1), 'r', label='reference')

ax2.plot(x_trajectory2, y_trajectory2, 'g', label='P controller')
ax2.plot(x_trajectory2, np.zeros(n2), 'r', label='reference')

plt.show()
