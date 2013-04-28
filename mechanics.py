###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: mechanics.py
# Author: Ken Sheedlo
#
# Orbital mechanics equations.
#
###############################################################################

from __future__ import division

import numpy

def twobody(gravity, m1, m2):
    '''
    Constructs the two-body problem.

    The state of the system should be specified as a 12-vector x containing the 
    position and velocity of the first body respectively, followed by the 
    position and velocity of the second body likewise. All positions and 
    velocities are considered to be vectors in 3-space, for a total of 12 
    coordinates.

    Parameters:
        gravity The gravitational constant G.
        m1      Mass of the first body.
        m2      Mass of the second body.

    Returns: a callable df(t, x) that returns the value of the derivative of
                the system at time t and state x. Note that the system is 
                autonomous, therefore t is always discarded. It is included for 
                compatibility with ODE solvers.
    '''
    def _twobody(_, st):
        rdisp = st[:3] - st[6:9]
        # Performance optimization: Factor equations as much as possible
        common = gravity*rdisp/(rdisp.dot(rdisp) ** (3/2))
        dv1 = -m2*common
        dv2 = m1*common
        return numpy.concatenate((st[3:6], dv1, st[9:], dv2))
    return _twobody
