###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: dimension.py
# Author: Ken Sheedlo
#
# Algorithms for computing the dimension of chaotic attractors.
#
###############################################################################

from __future__ import division

import multiprocessing
import numpy

def _capacity_n(xs, x0, eps):
    grid = set([tuple([int((xi-x0[i]) / eps) for (i, xi) in enumerate(xv)])
                for xv in xs])
    return len(grid)

def _capacity_for_tuple(arg):
    return _capacity_n(arg[0], arg[1], arg[2])

def capacity(xs, x0, epss):
    pool = multiprocessing.Pool()
    pargs = [(xs, x0, eps) for eps in epss]
    n_epss = pool.map(_capacity_for_tuple, pargs)
    pool.close()
    return numpy.array(zip([1.0 / eps for eps in epss], n_epss), dtype=numpy.float64)
