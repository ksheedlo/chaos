###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: chaostest.py
# Author: Ken Sheedlo
#
# Testing facilities for chaos programs.
#
###############################################################################

import unittest

from numpy.linalg import norm

class TestCase(unittest.TestCase):
    '''
    Extends the standard unittest TestCase with relevant asserts.

    '''
    def assertDataFits(self, ts, xs, func, **kwargs):
        '''
        Assert that (t, x) data points fit the given function.

        '''
        delta = kwargs.get('delta')
        places = kwargs.get('places')
        f_args = kwargs.get('f_args', tuple())

        assert_kwargs = dict()
        if delta is not None:
            assert_kwargs['delta'] = delta
        elif places is not None:
            assert_kwargs['places'] = places

        for (t_i, x_i) in zip(ts, xs):
            x_diff = norm(x_i - func(t_i, *f_args))
            self.assertAlmostEqual(delta, 0.0, **assert_kwargs)
