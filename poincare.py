###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: poincare.py
# Author: Ken Sheedlo
#
# Poincare section taker, PS6 stuff
#
###############################################################################

from __future__ import division

import chaostest
import getopt
import numpy
import plot
import rungekutta
import sys
import unittest

def section(ts, xs, interval=1.0, t_start=0.0):
    '''
    Simple, stupid Poincare section routine.

    '''
    t_final = ts[-1]
    p_ct = int((t_final+interval - t_start) / interval)
    ps = t_start + numpy.array(range(p_ct+1), dtype=numpy.float64) * interval
    i = 0
    j = 0
    points = numpy.empty((len(xs), xs[0].size), dtype=numpy.float64)
    for (ti, tj, x) in zip(ts[:-1], ts[1:], xs[1:]):
        while ps[i] < ti and i <= p_ct:
            i += 1
        if i > p_ct:
            break
        if ti < ps[i] and ps[i] <= tj:
            points[j] = x
            j += 1
    return points[:j]    

def linear(ts, xs, interval=1.0, t_start=0.0):
    '''
    Slightly smarter section routine, that linear interpolate frobs.

    '''
    t_final = ts[-1]
    p_ct = int((t_final+interval - t_start) / interval)
    ps = t_start + numpy.array(range(p_ct+1), dtype=numpy.float64) * interval
    i = 0
    j = 0
    points = numpy.empty((len(xs), xs[0].size), dtype=numpy.float64)
    for (ti, tj, xi, xj) in zip(ts[:-1], ts[1:], xs[:-1], xs[1:]):
        while ps[i] < ti and i <= p_ct:
            i += 1
        if i > p_ct:
            break
        if ti < ps[i] and ps[i] <= tj:
            dx = xj - xi
            points[j] = xi + dx*(ps[i]-ti)/(tj-ti)
            j += 1
    return points[:j]

class TestPoincare(chaostest.TestCase):
    '''
    Unit tests for Poincare section routines.

    '''
    def test_section(self):
        '''
        Tests the simple section routine with normal input.

        '''
        xs = numpy.array([1, 2, 42, 99, 1337, 23], dtype=numpy.float64)
        ts = numpy.array([1, 2, 3, 4, 5, 6], dtype=numpy.float64)
        ps = section(ts, xs, interval=2.0, t_start=1.5)
        self.assertArrayEqual(ps, xs[1::2])

    def test_linear(self):
        '''
        Tests the linear section routine with normal input.

        '''
        xs = numpy.array([1, 2, 42, 99, 1337, 23], dtype=numpy.float64)
        ts = numpy.array([1, 2, 3, 4, 5, 6], dtype=numpy.float64)
        ps = linear(ts, xs, interval=2.0, t_start=1.5)
        expected = numpy.array([1.5, 70.5, 680.0], dtype=numpy.float64)
        self.assertArrayEqual(ps, expected)

if __name__ == "__main__":
    unittest.main()