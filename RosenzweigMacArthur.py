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

def prey_change(ineff, drate, nutr, prey, pred):
    return (1-prey)*prey - (prey*pred)/(ineff+prey)

def pred_change(ineff, drate, nutr, prey, pred):
    return -drate*pred + nutr*(prey*pred)/(ineff+prey)

class RosenzweigMacArthur(System):
    def __init__(self, ineff, drate, nutr, prey0, pred0):
        # Rate of change of prey, specific to these parameters:
        spec_prey_change = functools.partial(prey_change,ineff,drate,nutr)
        # Rate of change of predator, specific to these parameters:
        spec_pred_change = functools.partial(pred_change,ineff,drate,nutr)
        System.__init__(self, prey0, pred0,
                        spec_prey_change, spec_pred_change)


