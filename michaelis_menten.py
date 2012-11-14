from __future__ import division

import sys
sys.path.append('.')

from diffyqs import FastSlowSystem

def enzyme_reaction(E0, S0, kp, km, k):
    s_change = lambda s, c: (E0/S0)*(km*c - kp*S0*s + kp*S0*c*s)
    c_change = lambda s, c: -(km+k)*c + kp*S0*s -kp*S0*c*s
    output = FastSlowSystem(1, 0, s_change, c_change)
    return output

r1 = enzyme_reaction(10**-6, .5, 10**6, 10**-6, 10**6)
r1.write(1.6, .005, 'temp/r1.csv')
