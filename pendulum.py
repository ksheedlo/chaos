###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: pendulum.py
# Author: Ken Sheedlo
#
# Pendulum problems for Problem Set 4.
#
###############################################################################

from __future__ import division

import getopt
import matplotlib.pyplot
import numpy
import rungekutta
import sys

from utils import split_dict, ufunc

PHASE_POINTS = (
        (3.0, 0.1),
        (2.6, 0.1),
        (0.1, 0.0),
        (0.2, 0.0),
        (-2*numpy.pi, 30.0),
        (-2*numpy.pi, 22.0),
        (2*numpy.pi, -30.0),
        (2*numpy.pi, -22.0),
        (numpy.pi/2, 0.0),
    )

def pendulum(mass, length, damping, ampl=0.0, freq=0.0):
    '''
    Creates a pendulum function.

    Parameters (all types are 64-bit floating point unless specified otherwise):
        mass        The mass of the simulated pendulum.
        length      The pendulum's length.
        damping     The damping coefficient.
        ampl        The drive amplitude (defaults to 0.0).
        freq        The drive frequency.

    Returns: a callable pfunc(t, x) that returns the value of the derivative at 
             t, x.
    '''
    def _pendulum(t, xvec):
        '''
        Pendulum callable function.

        '''
        theta = xvec[0]
        omega = xvec[1]
        omega_dot = (ampl*numpy.cos(freq*t) - damping*length*omega -
                    mass*9.8*numpy.sin(theta)) / (mass*length)
        return numpy.array([omega, omega_dot], dtype=numpy.float64)
    return _pendulum

def mod2pi(theta):
    modulus = int(numpy.floor(theta / (2*numpy.pi)))
    return theta - (modulus*2*numpy.pi)

def render_plot(ts, xs, *args, **kwargs):
    '''
    Renders a plot to the screen or to a file.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict((
                            'xlabel', 'ylabel', 'mod2pi', 'title', 'file_prefix'
                        ), kwargs)
    title = opts.get('title', '$x(t)$')
    file_prefix = opts.get('file_prefix')
    modulo = opts.get('mod2pi', False)

    axes.plot(ts, xs, *args, **plot_args)
    axes.set_xlabel(opts.get('xlabel', 't'))
    axes.set_ylabel(opts.get('ylabel', 'x'))
    axes.set_title(title)

    if modulo:
        axes.set_xbound(0, 2*numpy.pi)
        axes.set_xticks((
                    0, 
                    numpy.pi/2,
                    numpy.pi,
                    3*numpy.pi/2,
                    2*numpy.pi
                ))
        axes.set_xticklabels((
                    '0',
                    r'$\frac{\pi}{2}$',
                    r'$\pi$',
                    r'$\frac{3\pi}{2}$',
                    r'$2\pi$'
                ))

    if file_prefix is None:
        figure.show()
    else:
        figure.savefig('{0}.png'.format(file_prefix), dpi=220)

def make_phase_portrait(pfunc, *args, **kwargs):
    '''
    Constructs a phase portrait of the system.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(('title', 'file_prefix'), kwargs)
    file_prefix = opts.get('file_prefix')
    title = opts.get('title')

    for (theta, omega) in PHASE_POINTS:
        _, xs = rungekutta.rk4(
                                pfunc, 
                                0.0, 
                                numpy.array([theta, omega], dtype=numpy.float64),
                                0.005,
                                2000
                            )
        axes.plot(xs[0,:], xs[1,:], *args, **plot_args)

    axes.set_xlabel(r'$\theta$')
    axes.set_ylabel(r'$\omega$')
    axes.set_xbound(-3*numpy.pi/2, 3*numpy.pi/2)
    axes.set_xticks((
                -3*numpy.pi/2, 
                -numpy.pi, 
                -numpy.pi/2, 
                0, 
                numpy.pi/2,
                numpy.pi,
                3*numpy.pi/2
            ))
    axes.set_xticklabels((
                r'$-\frac{3\pi}{2}$',
                r'$-\pi$',
                r'$-\frac{\pi}{2}$',
                '0',
                r'$\frac{\pi}{2}$',
                r'$\pi$',
                r'$\frac{3\pi}{2}$'
            ))
    axes.set_title('Phase Portrait' if title is None else title)

    if file_prefix is None:
        figure.show()
    else:
        figure.savefig('{0}.png'.format(file_prefix), dpi=220)

def make_phase_portrait_mod2pi(pfunc, *args, **kwargs):
    '''
    Makes a phase portrait modulo 2*pi.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(('title', 'file_prefix'), kwargs)
    file_prefix = opts.get('file_prefix')
    title = opts.get('title')

    for (theta, omega) in PHASE_POINTS:
        _, xs = rungekutta.rk4(
                                pfunc, 
                                0.0, 
                                numpy.array([theta, omega], dtype=numpy.float64),
                                0.005,
                                2000
                            )
        xs[0,:] = numpy.array([
                            mod2pi(theta) for theta in xs[0,:]
                        ], dtype=numpy.float64)
        axes.plot(xs[0,:], xs[1,:], *args, **plot_args)

    axes.set_xlabel(r'$\theta$')
    axes.set_ylabel(r'$\omega$')
    axes.set_xbound(0, 2*numpy.pi)
    axes.set_xticks((
                0, 
                numpy.pi/2,
                numpy.pi,
                3*numpy.pi/2,
                2*numpy.pi
            ))
    axes.set_xticklabels((
                '0',
                r'$\frac{\pi}{2}$',
        import pdb; pdb.set_trace()
                r'$\pi$',
                r'$\frac{3\pi}{2}$',
                r'$2\pi$'
            ))
    axes.set_title('Phase Portrait' if title is None else title)

    if file_prefix is None:
        figure.show()
    else:
        figure.savefig('{0}.png'.format(file_prefix), dpi=220)

def plot_pfunc(pfunc, *args, **kwargs):
    '''
    Convenience function for experimenting with pendulum functions.

    '''
    opts, plot_args = split_dict(('tstep', 'theta0', 'omega0', 'nsteps'), kwargs)
    theta0 = opts.get('theta0', 3.0)
    omega0 = opts.get('omega0', 0.1)
    tstep = opts.get('tstep', 0.005)
    nsteps = opts.get('nsteps', 2000)
    _, xs = rungekutta.rk4(
                        pfunc, 
                        0.0, 
                        numpy.array([theta0, omega0], dtype=numpy.float64),
                        tstep, 
                        nsteps
                    )
    fix_domain = lambda x: mod2pi(x) if kwargs.get('mod2pi', False) else x
    xs[0,:] = numpy.array([
                        fix_domain(theta) for theta in xs[0,:]
                    ], dtype=numpy.float64)
    render_plot(xs[0,:], xs[1,:], *args, **plot_args)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    file_prefix = None

    try:
        options, args = getopt.getopt(argv[1:], 'f:')
        for opt, arg in options:
            if opt == '-f':
                file_prefix = arg
    except getopt.GetoptError as err:
        print str(err)
        return 2

    suffixed = lambda s, suf: None if s is None else '{0}{1}'.format(s, suf)

    pfunc = pendulum(0.1, 0.1, 0)
    ts, xs = rungekutta.rk4(
                            pfunc, 
                            0.0, 
                            numpy.array([3.0, 0.1], dtype=numpy.float64), 
                            0.005, 
                            2000
                        )
    render_plot(xs[0,:], 
                xs[1,:], 
                title='Undriven, Undamped Pendulum', 
                file_prefix=suffixed(file_prefix, '_2a'),
                xlabel=r'$\theta$',
                ylabel=r'$\omega$'
                )

    ts1, xs1 = rungekutta.rk4(
                            pfunc,
                            0.0,
                            numpy.array([0.01, 0.0], dtype=numpy.float64),
                            0.005,
                            2000
                        )
    render_plot(xs1[0,:], 
                xs1[1,:], 
                title='Undriven, Undamped Pendulum',
                file_prefix=suffixed(file_prefix, '_2b'),
                xlabel=r'$\theta$',
                ylabel=r'$\omega$'
                )

    make_phase_portrait(
            pfunc, 
            'b',
            title=r'Phase Portrait ($m=0.1, l=0.1, \beta=0)$', 
            file_prefix=suffixed(file_prefix, '_3')
        )

    pfunc2 = pendulum(0.1, 0.1, 0.25)
    make_phase_portrait(
            pfunc2, 
            'b',
            title=r'Phase Portrait ($m=0.1, l=0.1, \beta=0.25)$', 
            file_prefix=suffixed(file_prefix, '_4')
        )

    make_phase_portrait_mod2pi(
            pfunc2, 
            'b.',
            title=r'Phase Portrait ($m=0.1, l=0.1, \beta=0.25)$ Mod $2\pi$', 
            file_prefix=suffixed(file_prefix, '_5'),
            markersize=0.6
        )

    return 0

if __name__ == "__main__":
    sys.exit(main())