import copy
import numpy as np
import math

class Frame(object):
    def __init__(self, t, r, v):
        self.t = t
        self.r = r
        self.v = v

class Particle(object):
    def __init__(self, r0, v0):
        self.framelist = list()
        self.add_frame(0,r0,v0)
    
    def position(self, t):
        startframe = None
        for index, frame in enumerate(self.framelist):
            if frame.t > t:
                startframe = framelist[index - 1]
                break
        if startframe is None:
            raise ValueError('that part of the trajectory has not\
                             yet been calculated')
        return (t - startframe.t)*startframe.v + startframe.r

    def add_frame(self, t, r, v):
        self.framelist.append(Frame(t, r, v))


def collision(o1, o2, t):
    '''Add frames to two objects after a collision between them.'''
    
    f1 = o1.framelist[-1]
    f2 = o2.framelist[-1]
    if f1.t > t or f2.t > t:
        raise ValueError('already calculated at this t')
    # We're going to work in a new reference frame, where o1 has velocity
    # 0. Relative to the original reference frame, the origin moves
    # with velocity f1.v
    
    # Old velocity difference, and the velocity of o2 in the new
    # reference frame:
    dv = f2.v - f1.v

    # Find the vector that points from o1 to o2
    r1 = f1.r + (t - f1.t) * f1.v
    r2 = f2.r + (t - f2.t) * f2.v
    dr = r2 - r1


    # Make sure that there's actually a collision.
    # (the circles have radius 2)
    if abs(np.linalg.norm(dr)- 2) > .001:
        raise ValueError('no collision at this time')
    # This is not a perfect check though. If one of the particles 
    # has something in the way so that it will never really reach the
    # collision site, this won't detect it. You have to make sure
    # you always calculate the _first_ collision that happens.
    # If you don't, there will be no error message, only a subtly
    # nonsensical simulation.

    # Divide dv into a component along dr, and a perpendicular component
    dv_parr = (np.dot(dv, dr) / np.linalg.norm(dr)) * dv
    dv_perp = dv - dv_parr

    # Construct a new vector - the new velocity difference.
    du = dv_perp + -1*dv_parr
    
    # The velocity of the origin, relative to the original reference
    # frame, is f1.v.
    # Make a new velocity for the origin, such that momentum is
    # conserved:
    origin_v = f1.v + (-1*du)/2

    # Calculate the new velocities for each particle, relative
    # to the original reference frame
    u1 = origin_v + du
    u2 = origin_v

    # I don't know what the problem is, but these don't actually
    # conserve momentum

    # Add new frames
    o1.add_frame(t, r1, u1)
    o2.add_frame(t, r2, u2)
def time_until_collision(o1, o2):
    pass

x = Particle(np.zeros(2), np.zeros(2))
y = Particle(np.array([1.,1.]), np.array([-1.,-1.]))
backup = [copy.deepcopy(i) for i in (x, y)]

f1 = x.framelist[-1]
f2 = y.framelist[-1]
r1 = f1.r
r2 = f2.r + (2 - f2.t)*f2.v
collision(x, y, 1 + math.sqrt(2))
