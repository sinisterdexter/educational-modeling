from __future__ import division
import functools
import csv
from math import sqrt

class System(object):
    def __init__(self, x0, y0, f, g):
        self.x = x0
        self.y = y0
        self.f = f
        self.g = g
    
    def update(self, h):
        self.x = self.x + self.f(self.x, self.y)*h
        self.y = self.y + self.g(self.x, self.y)*h
        return (self.x, self.y)
    
    def write(self, t, h, output_path):
        '''Write a csv file of the dynamics over time t, calculated using
        time intervals of h, to output_path'''

        # Figure out how many iterations to do
        n = int(t/h)

        # Write the iterations to a csv file
        self._write(h, n, output_path)

    def _write(self, update_param, iterations, output_path):
        '''Private function called by write functions of System and
        derivative classes'''
        with open(output_path, 'wb') as f:
            writer = csv.writer(f)
            # Write initial state:
            csv.writer(f).writerow((self.x, self.y))
            # Write the next n states:
            csv.writer(f).writerows(self.update(update_param) \
                                     for i in xrange(iterations))
    
class FastSlowSystem(System):
    '''A differential equation that has dynamics on multiple time scales.
    System objects do Euler integration. FastSlowSystem objects, instead
    of having a fixed time step for each update, have a fixed distance in 
    phase space that is crossed.'''
    
    # This algorithm doesn't work for the update. The fast motion never
    # quite reaches a fixed point, it goes back and forth across it.
    # But then the algorithm spends all of its r rendering this back-and-
    # forth motion, and the slow movement never happens, the time scales
    # stay too short.
    def update(self, r):
        mx = self.f(self.x, self.y)
        my = self.g(self.x, self.y)
        h = sqrt(r**2 / (mx**2 + my**2))
        self.x = self.x + mx*h
        self.y = self.y + my*h
        return (self.x, self.y)

    def write(self, d, r, output_path):
        '''Write a csv file of the dynamics over distace d, calculated using
        points with spacing r, to output_path'''

        # Figure out how many iterations to do
        n = int(d/r)

        # Write the iterations to a csv file
        self._write(r, n, output_path)
