############################################################################### #
#
# CSCI 4446 - Chaotic Dynamics
# File: ps8.py
# Author: Ken Sheedlo
#
# Shared-nothing web scale corporate synergy policy
#
###############################################################################

from __future__ import division

import embed
import getopt
import numpy
import pendulum
import plot
import re
import sys

from differentiation import ndiff, ddiff
from utils import suffixed

def construct_angular_velocity(ts, xs):
    '''
    Builds a ndarray with ts, xs and angular velocity (omegas, oss).

    Abbreviate omegas as oss to avoid confusion with os, which is a Python 
    standard library module.

    Params:
        ts  The time values to differentiate over.
        xs  The theta values to differentiate.

    Returns:
        points  A (n x 3) ndarray, where the 0th column is ts, 1st is xs and
                2nd is oss.
    '''
    oss = ndiff(ts, xs)
    points = numpy.empty((len(ts), 3), dtype=numpy.float64)
    points[:,0] = ts
    points[:,1] = xs
    points[:,2] = oss
    return points

def pr1(file_prefix=None):
    data = numpy.loadtxt('data/ps8/data1', dtype=numpy.float64)
    points = construct_angular_velocity(data[::30,1], data[::30,0])
    thetas = numpy.array([
                    pendulum.mod2pi(theta) for theta in points[:,1]
                ], dtype=numpy.float64)
    plot.render(
            thetas, 
            points[:,2], 
            'b', 
            xlabel=r'$\theta$',
            ylabel=r'$\omega$',
            title='State-space Trajectory, Data Set 1',
            file_prefix=suffixed(file_prefix, '_1')
        )

def _get_actual_delay(dset, col, delay):
    dt = 0.002 if re.match('data2', dset) else 0.001
    return dt * col * delay

def embed_run(dset='data1', delay=150, vdim=7, xdim=0, ydim=1, file_prefix=None):
    '''
    Renders a parameterized delay coordinate embedding.

    '''
    data = numpy.loadtxt('data/ps8/{0}'.format(dset), dtype=numpy.float64)
    vs = embed.embed(data[:,0], delay, vdim)
    plot.embedded(
                vs, 
                xdim, 
                ydim, 
                'k.', 
                markersize=0.6, 
                ybound=(0, 2*numpy.pi),
                yticks=(
                        0,
                        numpy.pi/2,
                        numpy.pi,
                        3*numpy.pi/2,
                        2*numpy.pi
                    ),
                yticklabels=(
                        '0',
                        r'$\frac{\pi}{2}$',
                        r'$\pi$',
                        r'$\frac{3\pi}{2}$',
                        r'$2\pi$'
                    ),
                title=r'Delay Coordinate Embedding: {0}, $\tau={1}$'.format(
                                                dset, 
                                                _get_actual_delay(dset, 1, delay)),
                xlabel=r'$\theta(t + {0})$'.format(_get_actual_delay(dset, xdim, delay)),
                ylabel=r'$\theta(t + {0})$'.format(_get_actual_delay(dset, ydim, delay)),
                aspect='equal',
                file_prefix=file_prefix
            )

def pr2a(file_prefix=None):
    embed_run(dset='data2', delay=75, ydim=2, file_prefix=suffixed(file_prefix, '_2a'))

def main(argv=None):
    if argv is None:
        argv = sys.argv

    file_prefix = None

    def pr2b(file_prefix, delay, dim):
        embed_run(
                dset='data3', 
                delay=delay, 
                vdim=dim, 
                ydim=5, 
                file_prefix=suffixed(file_prefix, '_2b')
            )

    ops = 'ab'
    delay = 10
    dim = 7

    try:
        options, args = getopt.getopt(argv[1:], 'f:p:d:v:')
        for opt, arg in options:
            if opt == '-f':
                file_prefix = arg 
            if opt == '-p':
                ops = arg
            if opt == '-d':
                delay = int(arg)
            if opt == '-v':
                dim = int(arg)
    except getopt.GetoptError as err:
        print str(err)
        return 2

    if 'a' in ops:
        pr1(file_prefix=file_prefix)
    if 'b' in ops:
        pr2a(file_prefix=file_prefix)
    if 'c' in ops:
        pr2b(file_prefix, delay, dim)

    return 0

if __name__ == "__main__":
    sys.exit(main())
