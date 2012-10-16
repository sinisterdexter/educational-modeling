from matplotlib import pyplot as plt
import math

class PopulationModel(object):
    '''A representation of interacting populations.. General class that
    contains methods that would be the
    same for all population models, such as plotting methods.
    Classes inheriting from Population should have an __init__ method
    that sets the parameters and an update method that updates the
    populations being tracked.'''
    def plot_fixed_number(self, n):
        '''Run the population for n generations after the initial generation
        and plot the host and parasitoid populations on a plane'''
        pairs = [(self.N, self.P)] + [self.update() for i in range(n)]
        plt.plot([x[0] for x in pairs], [x[1] for x in pairs])
        #plt.plot(pairs)
        return pairs

    def plot_until_dead(self):
        '''Run the population until either the hosts or parasitoid populations
        are less than 1. Return number of updates performed'''
        pairs = [(self.N, self.P)]
        for i in xrange(10**6):
            pairs.append(self.update())
            if self.N < 1 or self.P < 1:
                break
        plt.plot([x[0] for x in pairs], [x[1] for x in pairs])
        return pairs
        
class NicholsonBaileyPop(PopulationModel):
    '''A population of parasitoids and their hosts that evolves as a Nicholson-
    Bailey model.
    Initialize with these parameters:
        lamb: host reproduction rate
        c: parasitoid reproduction rate
        a: host/parasitoid encounter probability
        N0: initial host population
        P0: initial parasitoid population'''
    def __init__(self, lamb, c, a, N0, P0):
        self.lamb = lamb
        self.c = c
        self.a = a
        self.N = N0
        self.P = P0

    def update(self):
        '''Update parasitoid and host populations acocrding to Nicholson-Bailey
        model; return tuple containing new host and parasitoid populations'''
        Nu = self.lamb * self.N * math.exp(-1 * self.a * self.P)
        Pu = self.c * self.N * (1 - math.exp(-1 * self.a * self.P))
        self.N = Nu
        self.P = Pu
        return (Nu, Pu)

unstable=NicholsonBaileyPop(1.1, 3, 2e-5, 1, 1)
stable  =NicholsonBaileyPop(0.9, 3, 2e-5, 1, 1)

