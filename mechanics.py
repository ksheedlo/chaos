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

def threebody(gravity, m1, m2, m3):
    """
    Constructs the three-body problem.

    The state of the system should be specified as a 18-vector x with the 
    position and velocity of each body. The order agrees with the format defined
    in the two-body equation. 

    Parameters:
        gravity The gravitational constant G.
        m1      Mass of the first body.
        m2      Mass of the second body.
        m3      Mass of the third body.

    Returns: a callable df(t, x) that returns the value of the derivative of the 
                system at time t and state x. The time parameter t is included 
                for compatibility with ODE solvers, although the system is 
                autonomous.
    """
    def _threebody(_, st):
        rdisp12 = st[:3] - st[6:9]
        rdisp13 = st[:3] - st[12:15]
        rdisp23 = st[6:9] - st[12:15]
        common12 = gravity*rdisp12/(rdisp12.dot(rdisp12) ** (3/2))
        common13 = gravity*rdisp13/(rdisp13.dot(rdisp13) ** (3/2))
        common23 = gravity*rdisp23/(rdisp23.dot(rdisp23) ** (3/2))
        dv1 = -m2*common12 - m3*common13
        dv2 = m1*common12 - m3*common23 
        dv3 = m1*common13 + m2*common23 
        return numpy.concatenate((st[3:6], dv1, st[9:12], dv2, st[15:], dv3))
    return _threebody
