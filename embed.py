###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: embed.py
# Author: Ken Sheedlo
#
# Delay coordinate embedding.
#
###############################################################################

from __future__ import division

import numpy
import chaostest
import unittest

def embed(xs, delay, dim):
    '''
    Embeds the X data and produces the corresponding trajectory.

    Parameters:
        xs      The data set to embed, as an (nx1) vector. Must be sampled with
                an evenly spaced interval.
        delay   The time interval to span, as an integer multiple of the
                sampling interval.
        dim     The dimension of the embed vectors.

    Returns:
        vs      An (n x dim) ndarray, where vs[i,j] = $\\theta$(t_j + i*delay).
    '''
    return numpy.array([
            xs[j:j+(dim*delay):delay] for j in xrange(len(xs)-(dim*delay)+1)
        ], dtype=numpy.float64)

class TestEmbed(chaostest.TestCase):
    '''
    Test suite for delay coordinate embedding module.

    '''
    def test_embed(self):
        '''
        Tests embed function under normal operation.

        '''
        xs = numpy.array(range(1, 8), dtype=numpy.float64)
        result = embed(xs, 2, 3)
        expected = numpy.array([
                            [1, 3, 5], 
                            [2, 4, 6], 
                            [3, 5, 7]
                        ], dtype=numpy.float64)
        for (rrow, xrow) in zip(result, expected):
            for (r, x) in zip(rrow, xrow):
                self.assertEquals(r, x)

if __name__ == "__main__":
    unittest.main()