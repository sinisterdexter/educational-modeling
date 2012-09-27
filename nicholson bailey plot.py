from matplotlib import pyplot as plt
import math

class Population(object):
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
        

x = Population(16, 2, 20 * 10**-3 * 10**-3, 10**5, 10**3)
output = x.plot_until_dead()
print(len(output))
