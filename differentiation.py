###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: differentiation.py
# Author: Ken Sheedlo
#
# Numerical differentiation routines.
#
###############################################################################

from __future__ import division

import numpy
import chaostest
import unittest

def ndiff(ts, xs):
    '''
    Computes the numerical derivative over arbitrary data with O(h^2) error.

    Where h is the spacing of the ts, this function uses a 3-point formula to
    compute dx/dt. t-values do not have to be evenly spaced. ts must have length
    at least 3.

    Source: Burden and Faires. Numerical Analysis, 8th edition. Chapter 4.1, 
            "Numerical Differentiation". 

    Params:
        ts  Time values for each data point.
        xs  X values for each data point. Must have the same length as ts.

    Returns: dxs a ndarray with the value of the derivative at each t.
    '''
    def _diff(ts, xs):
        return xs[0]*(ts[1]-ts[2])/((ts[0]-ts[1])*(ts[0]-ts[2])) + \
            xs[1]*(2*ts[1]-ts[0]-ts[2])/((ts[1]-ts[0])*(ts[1]-ts[2])) + \
            xs[2]*(ts[1]-ts[0])/((ts[2]-ts[0])*(ts[2]-ts[1]))

    ts_len = len(ts)
    dxs = numpy.empty(ts_len, dtype=numpy.float64)
    dxs[0] = xs[0]*(2*ts[0]-ts[1]-ts[2])/((ts[0]-ts[1])*(ts[0]-ts[2])) + \
                xs[1]*(ts[0]-ts[2])/((ts[1]-ts[0])*(ts[1]-ts[2])) + \
                xs[2]*(ts[0]-ts[1])/((ts[2]-ts[0])*(ts[2]-ts[1]))

    for i in xrange(1, ts_len-1):
        dxs[i] = _diff(ts[i-1:i+2], xs[i-1:i+2])

    dxs[-1] = xs[-3]*(ts[-1]-ts[-2])/((ts[-3]-ts[-2])*(ts[-3]-ts[-1])) + \
                xs[-2]*(ts[-1]-ts[-3])/((ts[-2]-ts[-3])*(ts[-2]-ts[-1])) + \
                xs[-1]*(2*ts[-1]-ts[-3]-ts[-2])/((ts[-1]-ts[-3])*(ts[-1]-ts[-2]))
    return dxs

def ddiff(ts, xs):
    '''
    Computes the numerical derivative using divided differences.

    This function is less accurate than ndiff above. It has O(h) error and uses
    a simpler formula. It is mainly useful for debugging problems with the more
    complicated ndiff. ts and xs must have length at least 2.

    Params:
        ts  Time values for each data point.
        xs  X values for each data point. Must have the same length as ts.

    Returns: dxs a ndarray with the value of the derivative at each t.
    '''
    ts_len = len(ts)
    dxs = numpy.empty(ts_len, dtype=numpy.float64)

    for i in xrange(ts_len-1):
        dxs[i] = (xs[i+1]-xs[i])/(ts[i+1]-ts[i])

    dxs[-1] = dxs[-2]    
    return dxs

class TestDifferentiation(chaostest.TestCase):
    '''
    Test suite for numerical differentiators.

    '''
    def test_ndiff(self):
        '''
        Tests the general numerical differentiator for correctness.

        '''
        ts = 0.01 * numpy.array(range(100), dtype=numpy.float64)
        xs = numpy.array([(t**2) for t in ts], dtype=numpy.float64)
        expected = 0.02 * numpy.array(range(100), dtype=numpy.float64)
        self.assertArrayEqual(ndiff(ts, xs), expected, places=4)

if __name__ == "__main__":
    unittest.main()