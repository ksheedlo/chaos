###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: ps6.py
# Author: Ken Sheedlo
#
# Super important PS6 program / frobozz kernel extensions
#
###############################################################################

from __future__ import division

import getopt
import numpy
import pendulum
import plot
import poincare
import rungekutta
import sys

def _suffixed(word, suf):
    return None if word is None else '{0}{1}'.format(word, suf)

def pr1a(file_prefix):
    pfunc = pendulum.pendulum(0.1, 0.1, 0)
    ts, xs = rungekutta.rk4(
                            pfunc, 
                            0.0,
                            numpy.array([0.01, 0.0], dtype=numpy.float64),
                            0.005,
                            80000
                        )
    points = xs.transpose()
    ps = poincare.section(ts, points, interval=0.6346975625940523)
    plot.render(
            ps[:,0], 
            ps[:,1], 
            'k.',
            xbound=(-0.015, 0.015),
            ybound=(-0.15, 0.15),
            xlabel=r'$\theta$', 
            ylabel=r'$\omega$', 
            markersize=0.6,
            title='Poincare Section (Natural Frequency)',
            file_prefix=_suffixed(file_prefix, '_1a')
        )
    return ts, points

def pr1b(file_prefix, ts, points):
    ps2 = poincare.section(ts, points, interval=0.51)
    plot.render(
            ps2[:,0],
            ps2[:,1],
            'k.',
            xbound=(-0.015, 0.015),
            ybound=(-0.15, 0.15),
            xlabel=r'$\theta$', 
            ylabel=r'$\omega$', 
            markersize=0.6,
            title='Poincare Section (Irrational Frequency)',
            file_prefix=_suffixed(file_prefix, '_1b')
        )

def pr1c(file_prefix):
    drive_freq = 7.4246
    pfunc2 = pendulum.pendulum(0.1, 0.1, 0.25, ampl=1, freq=drive_freq)
    ts2, xs2 = rungekutta.rk4(
                            pfunc2, 
                            0.0, 
                            numpy.array([3.0, 0.1], dtype=numpy.float64), 
                            0.005, 
                            1000000
                        )
    xs2[0,:] = numpy.array(
                        [pendulum.mod2pi(x) for x in xs2[0,:]], 
                        dtype=numpy.float64
                    )
    points2 = xs2.transpose()
    ps3 = poincare.section(ts2, points2, interval=2*numpy.pi/drive_freq)
    plot.mod2pi(
            ps3[:,0],
            ps3[:,1],
            'k.',
            xlabel=r'$\theta$', 
            ylabel=r'$\omega$', 
            markersize=0.6,
            title='Poincare Section (Chaotic Trajectory)',
            file_prefix=_suffixed(file_prefix, '_1c')
        )

def pr1d(file_prefix):
    drive_freq = 7.4246
    pfunc2 = pendulum.pendulum(0.1, 0.1, 0.25, ampl=1, freq=drive_freq)
    ts3, xs3 = rungekutta.rk4(
                            pfunc2,
                            0.0, 
                            numpy.array([3.0, 0.1], dtype=numpy.float64),
                            0.02,
                            250000
                        )
    xs3[0,:] = numpy.array(
                        [pendulum.mod2pi(x) for x in xs3[0,:]], 
                        dtype=numpy.float64
                    )
    points3 = xs3.transpose()
    ps4 = poincare.section(ts3, points3, interval=2*numpy.pi/drive_freq)
    plot.mod2pi(
            ps4[:,0],
            ps4[:,1],
            'k.',
            xlabel=r'$\theta$', 
            ylabel=r'$\omega$', 
            markersize=0.6,
            title='Poincare section, increased step size',
            file_prefix=_suffixed(file_prefix, '_1d')
        )

def pr2a(file_prefix):
    pr2x(file_prefix, 0.005, 1000000, 'Poincare section, linear interpolation', '_2a')

def pr2b(file_prefix):
    pr2x(file_prefix, 0.02, 250000, 'Poincare section, increased step size', '_2b')

def pr2x(file_prefix, step, nsteps, title, suffix):
    drive_freq = 7.4246
    pfunc = pendulum.pendulum(0.1, 0.1, 0.25, ampl=1.0, freq=drive_freq)
    ts, xs = rungekutta.rk4(
                            pfunc,
                            0.0,
                            numpy.array([3.0, 0.1], dtype=numpy.float64),
                            step,
                            nsteps
                        )
    xs[0,:] = numpy.array(
                        [pendulum.mod2pi(x) for x in xs[0,:]],
                        dtype=numpy.float64
                    )
    points = xs.transpose()
    ps = poincare.linear(ts, points, interval=2*numpy.pi/drive_freq)
    plot.mod2pi(
            ps[:,0],
            ps[:,1],
            'k.',
            xlabel=r'$\theta$', 
            ylabel=r'$\omega$', 
            markersize=0.6,
            title=title,
            file_prefix=_suffixed(file_prefix, suffix)
        )

def main(argv=None):
    if argv is None:
        argv = sys.argv

    file_prefix = None

    def aThenB(prefix):
        ts, points = pr1a(prefix)
        pr1b(prefix, ts, points)

    keyfuncs = (
            ('a', pr1a),
            ('b', aThenB),
            ('c', pr1c),
            ('d', pr1d),
            ('e', pr2a),
            ('f', pr2b)
        )
    ops = 'bcdef'

    try:
        options, args = getopt.getopt(argv[1:], 'f:p:')
        for opt, arg in options:
            if opt == '-f':
                file_prefix = arg
            if opt == '-p':
                ops = arg
    except getopt.GetoptError as err:
        print str(err)
        return 2

    if 'b' in ops:
        ops = ops.replace('a', '')

    for (key, op) in keyfuncs:
        if key in ops:
            op(file_prefix)

    return 0

if __name__ == "__main__":
    sys.exit(main())