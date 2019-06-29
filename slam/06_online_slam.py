#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# User Instructions
#
# In this problem you will implement a more manageable
# version of graph SLAM in 2 dimensions. 
#
# Define a function, online_slam, that takes 5 inputs:
# data, N, num_landmarks, motion_noise, and
# measurement_noise--just as was done in the last 
# programming assignment of unit 6. This function
# must return TWO matrices, mu and the final Omega.
#
# Just as with the quiz, your matrices should have x
# and y interlaced, so if there were two poses and 2
# landmarks, mu would look like:
#
# mu = matrix([[Px0],
#              [Py0],
#              [Px1],
#              [Py1],
#              [Lx0],
#              [Ly0],
#              [Lx1],
#              [Ly1]])
#
# Enter your code at line 566.

# -----------
# Testing
#
# You have two methods for testing your code.
#
# 1) You can make your own data with the make_data
#    function. Then you can run it through the
#    provided slam routine and check to see that your
#    online_slam function gives the same estimated
#    final robot pose and landmark positions.
# 2) You can use the solution_check function at the
#    bottom of this document to check your code
#    for the two provided test cases. The grading
#    will be almost identical to this function, so
#    if you pass both test cases, you should be
#    marked correct on the homework.
""" 

from math import *
import random

###########################################
class Matrix:
    """
    this is the matrix class
    we use it because it makes it easier to collect constraints in GraphSLAM
    and to calculate solutions (albeit inefficiently)
    """
    
    # implements basic operations of a matrix class

    def __init__(self, value = [[]]):
        """
        initialization - can be called with an initial matrix
        """
        self.value = value
        self.dimx  = len(value)
        self.dimy  = len(value[0])
        if value == [[]]:
            self.dimx = 0

    def zero(self, dimx, dimy = 0):
        """
        makes matrix of a certain size and sets each element to zero
        """
        if dimy == 0:
            dimy = dimx
        # check if valid dimensions
        if dimx < 1 or dimy < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.dimx  = dimx
            self.dimy  = dimy
            self.value = [[0.0 for col in range(dimy)] for row in range(dimx)]

    def identity(self, dim):
        """
        makes matrix of a certain (square) size and turns matrix into indentity matrix
        """
        # check if valid dimension
        if dim < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.dimx  = dim
            self.dimy  = dim
            self.value = [[0.0 for col in range(dim)] for row in range(dim)]
            for i in range(dim):
                self.value[i][i] = 1.0

    def show(self, txt = ''):
        """
        prints out values of matrix
        """
        for i in range(len(self.value)):
            print(txt + '['+ ', '.join('%.3f'%x for x in self.value[i]) + ']' )
        print(' ')

    def __add__(self, other):
        """
        defines element-wise matrix additon. Both matrices must be of equal dimensions
        """
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError("Matrices must be of equal dimension to add")
        else:
            # add if correct dimensions
            res = Matrix()
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res

    def __sub__(self, other):
        """
        defines element-wise matrix subtraction. Both matrices must be of equal dimensions
        """
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError("Matrices must be of equal dimension to subtract")
        else:
            # subtract if correct dimensions
            res = Matrix()
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res

    def __mul__(self, other):
        """
        defines multiplication. Both matrices must be of fitting dimensions
        """
        # check if correct dimensions
        if self.dimy != other.dimx:
            raise ValueError("Matrices must be m*n and n*p to multiply")
        else:
            # multiply if correct dimensions
            res = Matrix()
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimy):
                    for k in range(self.dimy):
                        res.value[i][j] += self.value[i][k] * other.value[k][j]
        return res

    def transpose(self):
        """
        compute a matrix transpose
        """
        res = Matrix()
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[j][i] = self.value[i][j]
        return res

    def take(self, list1, list2 = []):
        """
        creates a new matrix from the existing matrix elements.
        
        Example:
            l = matrix([[ 1,  2,  3,  4,  5], 
                        [ 6,  7,  8,  9, 10], 
                        [11, 12, 13, 14, 15]])
            l.take([0, 2], [0, 2, 3])
                
        results in:
              
            [[1, 3, 4], 
            [11, 13, 14]]
            
        take is used to remove rows and columns from existing matrices
        list1/list2 define a sequence of rows/columns that shall be taken
        is no list2 is provided, then list2 is set to list1 (good for symmetric matrices)
        """
        if list2 == []:
            list2 = list1
        if len(list1) > self.dimx or len(list2) > self.dimy:
            raise ValueError("list invalid in take()")

        res = Matrix()
        res.zero(len(list1), len(list2))
        for i in range(len(list1)):
            for j in range(len(list2)):
                res.value[i][j] = self.value[list1[i]][list2[j]]
        return res

    def expand(self, dimx, dimy, list1, list2 = []):
        """
        creates a new matrix from the existing matrix elements.
        
        Example:
            l = matrix([[1, 2, 3],
                        [4, 5, 6]])
            l.expand(3, 5, [0, 2], [0, 2, 3])
                
        results in:
            [[1, 0, 2, 3, 0], 
             [0, 0, 0, 0, 0], 
             [4, 0, 5, 6, 0]]
        
        expand is used to introduce new rows and columns into an existing matrix
        list1/list2 are the new indexes of row/columns in which the matrix
        elements are being mapped. Elements for rows and columns 
        that are not listed in list1/list2 
        will be initialized by 0.0.
        """
        if list2 == []:
            list2 = list1
        if len(list1) > self.dimx or len(list2) > self.dimy:
            raise ValueError("list invalid in expand()")

        res = Matrix()
        res.zero(dimx, dimy)
        for i in range(len(list1)):
            for j in range(len(list2)):
                res.value[list1[i]][list2[j]] = self.value[i][j]
        return res

    def Cholesky(self, ztol= 1.0e-5):
        """
        Computes the upper triangular Cholesky factorization of  
        a positive definite matrix.
        This code is based on http://adorio-research.org/wordpress/?p=4560
        """
        res = Matrix()
        res.zero(self.dimx, self.dimx)

        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else: 
                if d < 0.0:
                    raise ValueError("Matrix not positive-definite")
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(i)])
                if abs(S) < ztol:
                    S = 0.0
                try:
                   res.value[i][j] = (self.value[i][j] - S)/res.value[i][i]
                except:
                   raise ValueError("Zero diagonal")
        return res 
 
    def CholeskyInverse(self):
        """
        Computes inverse of matrix given its Cholesky upper Triangular
        decomposition of matrix.
        This code is based on http://adorio-research.org/wordpress/?p=4560
        """
        res = Matrix()
        res.zero(self.dimx, self.dimx)

        # Backward step for inverse.
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k]*res.value[j][k] for k in range(j+1, self.dimx)])
            res.value[j][j] = 1.0/ tjj**2 - S/ tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = \
                    -sum([self.value[i][k]*res.value[k][j] for k in \
                              range(i+1,self.dimx)])/self.value[i][i]
        return res
    
    def inverse(self):
        """
        comutes and returns the inverse of a square matrix
        """
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res

    def __repr__(self):
        """
        prints matrix
        """
        return repr(self.value)

###########################################
class Robot:
    """
    this is the robot class
    
    our robot lives in x-y space, and its motion is
    pointed in a random direction. It moves on a straight line
    until is comes close to a wall at which point it turns
    away from the wall and continues to move.

    For measurements, it simply senses the x- and y-distance
    to landmarks. This is different from range and bearing as 
    commonly studied in the literature, but this makes it much
    easier to implement the essentials of SLAM without
    cluttered math
    """


    def __init__(self, world_size = 100.0, measurement_range = 30.0,
                 motion_noise = 1.0, measurement_noise = 1.0):
        """
        creates robot and initializes location to 0, 0
        """
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.landmarks = []
        self.num_landmarks = 0

    def rand(self):
        return random.random() * 2.0 - 1.0

    def make_landmarks(self, num_landmarks):
        """
        make random landmarks located in the world
        """
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append([round(random.random() * self.world_size),
                                   round(random.random() * self.world_size)])
        self.num_landmarks = num_landmarks

    def move(self, dx, dy):
        """
        attempts to move robot by dx, dy. If outside world boundary, then the move does
        nothing and instead returns failure
        """
        x = self.x + dx + self.rand() * self.motion_noise
        y = self.y + dy + self.rand() * self.motion_noise

        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True

    def sense(self):
        """
        returns x- and y- distances to landmarks within visibility range
        because not all landmarks may be in this range, the list of measurements
        is of variable length. Set measurement_range to -1 if you want all
        landmarks to be visible at all times
        """
        Z = []
        for i in range(self.num_landmarks):
            dx = self.landmarks[i][0] - self.x + self.rand() * self.measurement_noise
            dy = self.landmarks[i][1] - self.y + self.rand() * self.measurement_noise    
            if self.measurement_range < 0.0 or abs(dx) + abs(dy) <= self.measurement_range:
                Z.append([i, dx, dy])
        return Z

    def __repr__(self):
        """
        print robot location
        """
        return 'Robot: [x=%.5f y=%.5f]'  % (self.x, self.y)

# ######################################################################
# ######################################################################
# ######################################################################

def make_data(N, num_landmarks, world_size, measurement_range, motion_noise, 
              measurement_noise, distance):
    """
    makes the robot data
    """
    complete = False

    while not complete:
        data = []

        # make robot and landmarks
        r = Robot(world_size, measurement_range, motion_noise, measurement_noise)
        r.make_landmarks(num_landmarks)
        seen = [False for row in range(num_landmarks)]
    
        # guess an initial motion
        orientation = random.random() * 2.0 * pi
        dx = cos(orientation) * distance
        dy = sin(orientation) * distance
    
        for k in range(N-1):
            # sense
            Z = r.sense()

            # check off all landmarks that were observed 
            for i in range(len(Z)):
                seen[Z[i][0]] = True
    
            # move
            while not r.move(dx, dy):
                # if we'd be leaving the robot world, pick instead a new direction
                orientation = random.random() * 2.0 * pi
                dx = cos(orientation) * distance
                dy = sin(orientation) * distance

            # memorize data
            data.append([Z, [dx, dy]])

        # we are done when all landmarks were observed; otherwise re-run
        complete = (sum(seen) == num_landmarks)

    print(' ')
    print('Landmarks: ', r.landmarks)
    print(r)

    return data
    

def print_result(N, num_landmarks, result):
    """
    print the result of SLAM, the robot pose(s) and the landmarks
    """
    print()
    print('Estimated Pose(s):')
    for i in range(N):
        print('    ['+ ', '.join('%.3f'%x for x in result.value[2*i]) + ', ' \
            + ', '.join('%.3f'%x for x in result.value[2*i+1]) +']')
    print()
    print('Estimated Landmarks:')
    for i in range(num_landmarks):
        print('    ['+ ', '.join('%.3f'%x for x in result.value[2*(N+i)]) + ', ' \
            + ', '.join('%.3f'%x for x in result.value[2*(N+i)+1]) +']')


# ######################################################################
# ######################################################################
def slam(data, N, num_landmarks, motion_noise, measurement_noise):
    """
    retains entire path and all landmarks
    """
    # set the dimension for the filter
    dim = 2 * (N + num_landmarks)

    # make the constraint information matrix and vector
    omega = Matrix()
    omega.zero(dim, dim)
    omega.value[0][0] = 1
    omega.value[1][1] = 1

    xi = Matrix()
    xi.zero(dim, 1)
    xi.value[0][0] = world_size / 2
    xi.value[1][0] = world_size / 2

    # process the data
    for k in range(len(data)):
        # n is the index of the robot pose in the matrix/vector
        n = k * 2

        measurement = data[k][0]
        motion = data[k][1]

        # integrate the measurements
        for i in range(len(measurement)):

            # m is the index of the landmark coordinate in the matrix/vector
            m = 2 * (N + measurement[i][0])

            # update the information matrix/vector based on the measurement
            for b in range(2):
                omega.value[n+b][n+b] += 1 / measurement_noise
                omega.value[m+b][m+b] += 1 / measurement_noise
                omega.value[n+b][m+b] += -1 / measurement_noise
                omega.value[m+b][n+b] += -1 / measurement_noise
                xi.value[n+b][0] += -measurement[i][1+b] / measurement_noise
                xi.value[m+b][0] += measurement[i][1+b] / measurement_noise

        # update the information matrix/vector based on the robot motion
        for b in range(4):
            omega.value[n+b][n+b] += 1 / motion_noise
        for b in range(2):
            omega.value[n+b][n+b+2] += -1 / motion_noise
            omega.value[n+b+2][n+b] += -1 / motion_noise
            xi.value[n+b][0] += -motion[b] / motion_noise
            xi.value[n+b+2][0] += motion[b] / motion_noise
    
    # compute best estimate
    mu = omega.inverse() * xi

    # return the result
    return mu 

# ######################################################################
def online_slam(data, N, num_landmarks, motion_noise, measurement_noise):
    """
    retains all landmarks but only most recent robot pose
    """
    # set the dimension for the filter
    dim = 2 * (1 + num_landmarks)

    # make the constraint information matrix and vector
    omega = Matrix()
    omega.zero(dim, dim)
    omega.value[0][0] = 1
    omega.value[1][1] = 1

    xi = Matrix()
    xi.zero(dim, 1)
    xi.value[0][0] = world_size / 2
    xi.value[1][0] = world_size / 2

    # process the data
    for k in range(len(data)):

        measurement = data[k][0]
        motion = data[k][1]

        # integrate the measurements
        for i in range(len(measurement)):

            # m is the index of the landmark coordinate in the matrix/vector
            m = 2 * (1 + measurement[i][0])

            # update the information matrix/vector based on the measurement
            for b in range(2):
                omega.value[b][b] += 1 / measurement_noise
                omega.value[m+b][m+b] += 1 / measurement_noise
                omega.value[b][m+b] += -1 / measurement_noise
                omega.value[m+b][b] += -1 / measurement_noise
                xi.value[b][0] += -measurement[i][1+b] / measurement_noise
                xi.value[m+b][0] += measurement[i][1+b] / measurement_noise

        # expand the information matrix and vector by one new position
        list = [0, 1] + [x for x in range(4, dim+2)]
        omega = omega.expand(dim+2, dim+2, list, list)
        xi = xi.expand(dim+2, 1, list, [0])

        # update the information matrix/vector based on the robot motion
        for b in range(4):
            omega.value[b][b] += 1 / motion_noise
        for b in range(2):
            omega.value[b][b+2] += -1 / motion_noise
            omega.value[b+2][b] += -1 / motion_noise
            xi.value[b][0] += -motion[b] / motion_noise
            xi.value[b+2][0] += motion[b] / motion_noise

        # new factor out the previous pose
        newlist = range(2, len(omega.value))
        a = omega.take([0, 1], newlist)
        b = omega.take([0, 1])
        c = xi.take([0, 1], [0])
        omega = omega.take(newlist) - a.transpose() * b.inverse() * a
        xi = xi.take(newlist, [0]) - a.transpose() * b.inverse() * c
    
    # compute best estimate
    mu = omega.inverse() * xi

    # return the result
    return mu, omega


# ######################################################################
# ######################################################################
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

num_landmarks      = 5        # number of landmarks
N                  = 20       # time steps
world_size         = 100.0    # size of world
measurement_range  = 50.0     # range at which we can sense landmarks
motion_noise       = 2.0      # noise in robot motion
measurement_noise  = 2.0      # noise in the measurements
distance           = 20.0     # distance by which robot (intends to) move each iteratation 

# The following three lines to run the full slam routine.

data = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
print("data:", data)
result = slam(data, N, num_landmarks, motion_noise, measurement_noise)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
print_result(N, num_landmarks, result)
print("**************************")

# The following three lines to run the online_slam routine.

# data = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
result = online_slam(data, N, num_landmarks, motion_noise, measurement_noise)
print_result(1, num_landmarks, result[0])

##########################################################

# ------------
# TESTING
#
# Uncomment one of the test cases below to check that your
# online_slam function works as expected.

def solution_check(result, answer_mu, answer_omega):

    if len(result) != 2:
        print("Your function must return TWO matrices, mu and Omega")
        return False
    
    user_mu = result[0]
    user_omega = result[1]
    
    if user_mu.dimx == answer_omega.dimx and user_mu.dimy == answer_omega.dimy:
        print("It looks like you returned your results in the wrong order. Make sure to return mu then Omega.")
        return False
    
    if user_mu.dimx != answer_mu.dimx or user_mu.dimy != answer_mu.dimy:
        print("Your mu matrix doesn't have the correct dimensions. Mu should be a", answer_mu.dimx, " x ", answer_mu.dimy, "matrix.")
        return False
    else:
        print("Mu has correct dimensions.")
        
    if user_omega.dimx != answer_omega.dimx or user_omega.dimy != answer_omega.dimy:
        print("Your Omega matrix doesn't have the correct dimensions. Omega should be a", answer_omega.dimx, " x ", answer_omega.dimy, "matrix.")
        return False
    else:
        print("Omega has correct dimensions.")
        
    if user_mu != answer_mu:
        print("Mu has incorrect entries.")
        return False
    else:
        print("Mu correct.")
        
    if user_omega != answer_omega:
        print("Omega has incorrect entries.")
        return False
    else:
        print("Omega correct.")
        
    print("Test case passed!")
    return True

# -----------
# Test Case 1

testdata1          = [[[[1, 21.796713239511305, 25.32184135169971], [2, 15.067410969755826, -27.599928007267906]], [16.4522379034509, -11.372065246394495]],
                      [[[1, 6.1286996178786755, 35.70844618389858], [2, -0.7470113490937167, -17.709326161950294]], [16.4522379034509, -11.372065246394495]],
                      [[[0, 16.305692184072235, -11.72765549112342], [2, -17.49244296888888, -5.371360408288514]], [16.4522379034509, -11.372065246394495]],
                      [[[0, -0.6443452578030207, -2.542378369361001], [2, -32.17857547483552, 6.778675958806988]], [-16.66697847355152, 11.054945886894709]]]

answer_mu1         = Matrix([[81.63549976607898],
                             [27.175270706192254],
                             [98.09737507003692],
                             [14.556272940621195],
                             [71.97926631050574],
                             [75.07644206765099],
                             [65.30397603859097],
                             [22.150809430682695]])

answer_omega1      = Matrix([[0.36603773584905663, 0.0, -0.169811320754717, 0.0, -0.011320754716981133, 0.0, -0.1811320754716981, 0.0],
                             [0.0, 0.36603773584905663, 0.0, -0.169811320754717, 0.0, -0.011320754716981133, 0.0, -0.1811320754716981],
                             [-0.169811320754717, 0.0, 0.6509433962264151, 0.0, -0.05660377358490567, 0.0, -0.40566037735849064, 0.0],
                             [0.0, -0.169811320754717, 0.0, 0.6509433962264151, 0.0, -0.05660377358490567, 0.0, -0.40566037735849064],
                             [-0.011320754716981133, 0.0, -0.05660377358490567, 0.0, 0.6962264150943396, 0.0, -0.360377358490566, 0.0],
                             [0.0, -0.011320754716981133, 0.0, -0.05660377358490567, 0.0, 0.6962264150943396, 0.0, -0.360377358490566],
                             [-0.1811320754716981, 0.0, -0.4056603773584906, 0.0, -0.360377358490566, 0.0, 1.2339622641509433, 0.0],
                             [0.0, -0.1811320754716981, 0.0, -0.4056603773584906, 0.0, -0.360377358490566, 0.0, 1.2339622641509433]])

#result = online_slam(testdata1, 5, 3, 2.0, 2.0)
#solution_check(result, answer_mu1, answer_omega1)


# -----------
# Test Case 2

testdata2          = [[[[0, 12.637647070797396, 17.45189715769647], [1, 10.432982633935133, -25.49437383412288]], [17.232472057089492, 10.150955955063045]],
                      [[[0, -4.104607680013634, 11.41471295488775], [1, -2.6421937245699176, -30.500310738397154]], [17.232472057089492, 10.150955955063045]],
                      [[[0, -27.157759429499166, -1.9907376178358271], [1, -23.19841267128686, -43.2248146183254]], [-17.10510363812527, 10.364141523975523]],
                      [[[0, -2.7880265859173763, -16.41914969572965], [1, -3.6771540967943794, -54.29943770172535]], [-17.10510363812527, 10.364141523975523]],
                      [[[0, 10.844236516370763, -27.19190207903398], [1, 14.728670653019343, -63.53743222490458]], [14.192077112147086, -14.09201714598981]]]

answer_mu2         = Matrix([[63.37479912250136],
                             [78.17644539069596],
                             [61.33207502170053],
                             [67.10699675357239],
                             [62.57455560221361],
                             [27.042758786080363]])

answer_omega2      = Matrix([[0.22871751620895048, 0.0, -0.11351536555795691, 0.0, -0.11351536555795691, 0.0],
                             [0.0, 0.22871751620895048, 0.0, -0.11351536555795691, 0.0, -0.11351536555795691],
                             [-0.11351536555795691, 0.0, 0.7867205207948973, 0.0, -0.46327947920510265, 0.0],
                             [0.0, -0.11351536555795691, 0.0, 0.7867205207948973, 0.0, -0.46327947920510265],
                             [-0.11351536555795691, 0.0, -0.46327947920510265, 0.0, 0.7867205207948973, 0.0],
                             [0.0, -0.11351536555795691, 0.0, -0.46327947920510265, 0.0, 0.7867205207948973]])

#result = online_slam(testdata2, 6, 2, 3.0, 4.0)
#solution_check(result, answer_mu2, answer_omega2)


