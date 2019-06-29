#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# User Instructions
#
# Modify your doit function to incorporate 3
# distance measurements to a landmark(Z0, Z1, Z2).
# You should use the provided expand function to
# allow your Omega and Xi matrices to accomodate
# the new information.
#
# Each landmark measurement should modify 4
# values in your Omega matrix and 2 in your
# Xi vector.
#
""" 

from math import *
import random

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



# ######################################################################
# ######################################################################
# ######################################################################


"""
For the following example, you would call doit(-3, 5, 3, 10, 5, 2):
3 robot positions
  initially: -3 (measure landmark to be 10 away)
  moves by 5 (measure landmark to be 5 away)
  moves by 3 (measure landmark to be 2 away)

  

which should return a mu of:
[[-3.0],
 [2.0],
 [5.0],
 [7.0]]
"""
def doit(initial_pos, move1, move2, sense0, sense1, sense2):
    omega = Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    xi = Matrix([[initial_pos], [0], [0]])

    omega += Matrix([[1, -1, 0], [-1, 1, 0], [0, 0, 0]])
    xi += Matrix([[-move1], [move1], [0]])

    omega += Matrix([[0, 0, 0], [0, 1, -1], [0, -1, 1]])
    xi += Matrix([[0], [-move2], [move2]])

    omega = omega.expand(4, 4, [0, 1, 2], [0, 1, 2])
    xi = xi.expand(4, 1, [0, 1, 2], [0])

    omega += Matrix([[1, 0, 0, -1], 
                     [0, 0, 0, 0], 
                     [0, 0, 0, 0], 
                     [-1, 0, 0, 1]])
    xi += Matrix([[-sense0], [0], [0], [sense0]])

    omega += Matrix([[0, 0, 0, 0], 
                     [0, 1, 0, -1], 
                     [0, 0, 0, 0], 
                     [0, -1, 0, 1]])
    xi += Matrix([[0], [-sense1], [0], [sense1]])

    omega += Matrix([[0, 0, 0, 0], 
                     [0, 0, 0, 0], 
                     [0, 0, 1, -1], 
                     [0, 0, -1, 1]])
    xi += Matrix([[0], [0], [-sense2], [sense2]])

    omega.show("Omega: ")
    xi.show("Xi:    ")
    mu = omega.inverse() * xi
    mu.show("Result: ")
    return mu

doit(-3, 5, 3, 10, 5, 1)
