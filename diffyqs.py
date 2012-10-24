from __future__ import division
import functools
import csv

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
        with open(output_path, 'wb') as f:
            writer = csv.writer(f)
            # Write initial state:
            csv.writer(f).writerow((self.x, self.y))
            # Write the next n states:
            csv.writer(f).writerows(self.update(h) for i in xrange(n))

