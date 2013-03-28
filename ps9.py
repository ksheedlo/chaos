###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
# File: ps9.py
# Author: Ken Sheedlo
#
# People-oriented Privateering IPO (IPA)
#
###############################################################################

from __future__ import division

import getopt
import lorenz
import numpy
import plot
import re
import rungekutta
import sys
import tispy

from numpy.linalg import eig
from ps7 import variational, ic, integrate
from utils import suffixed

def first_min(ms):
    for i in xrange(1, len(ms)-1):
        if ms[i,1] < ms[i+1,1]:
            return ms[i,0]
    return None

def pr2(delay=None, file_prefix=None):
    data = numpy.loadtxt('data/ps8/data2.first250sec', dtype=numpy.float64)
    if delay is not None:
        ms = tispy.mutual('-D', str(delay), input=data)
    else:
        ms = tispy.mutual(input=data)
    tau = first_min(ms)

    def _render(axes):
        axes.plot(ms[:,0], ms[:,1])
        (lbound, ubound) = axes.get_ybound()
        axes.plot([tau, tau], [lbound, ubound], 'k')
        axes.legend(('Mutual information', r'Optimal $\tau$'))

    plot.render(
            xlabel=r'$\tau$',
            ylabel='Mutual information',
            title=r'Mutual information vs. $\tau$ (min at $\tau$={0})'.format(first_min(ms)),
            ax_callback=_render,
            file_prefix=suffixed(file_prefix, '_1')
        )

def select_embedding_dimension(fnns):
    for fnn in fnns:
        if fnn[1] < 0.1:
            return fnn[0]
    return None

def pr3(file_prefix=None):
    data = numpy.loadtxt('data/ps8/data2.first250sec', dtype=numpy.float64)
    fnns = tispy.false_nearest('-M', '1,10', '-d', '155', input=data)
    dim = select_embedding_dimension(fnns)

    def _render(axes):
        axes.plot(fnns[:,0], fnns[:,1])
        axes.plot([dim, dim], axes.get_ybound(), 'k')
        axes.plot(axes.get_xbound(), [0.1, 0.1], 'k--')
        axes.legend((
                    'False nearest neighbors', 
                    r'Selected $m$',
                    r'$\leq$10% FNNs required'
                ))

    plot.render(
            xlabel=r'$m$',
            ylabel='Fraction of false nearest neighbors',
            title=r'False nearest neighbors vs. embedding dimension ($m$={0})'.format(
                        select_embedding_dimension(fnns)),
            ax_callback=_render,
            file_prefix=suffixed(file_prefix, '_2')
        )

def _get_actual_delay(dset, col, delay):
    dt = 0.002 if re.match('data2', dset) else 0.001
    return dt * col * delay

def cut(ts, xs):
    for i in xrange(len(ts)-1):
        if ts[i+1] < ts[i]:
            return (ts[:i+1], xs[:i+1]) + cut(ts[i+1:], xs[i+1:]) 
    return (ts, xs)

def pr4(file_prefix=None):
    data = numpy.loadtxt('data/ps8/data2.first250sec', dtype=numpy.float64)
    vs = tispy.delay('-d', '155', '-m', '8', input=data)
    plot.embedded(
                vs, 
                0, 
                2, 
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
                title=r'Delay Coordinate Embedding: {0}, $\tau={1}$ s'.format(
                                                'data2', 
                                                _get_actual_delay('data2', 1, 155)),
                xlabel=r'$\theta(t + {0})$'.format(_get_actual_delay('data2', 0, 155)),
                ylabel=r'$\theta(t + {0})$'.format(_get_actual_delay('data2', 2, 155)),
                aspect='equal',
                file_prefix=suffixed(file_prefix, '_3')
            )

def pr5(dim=8, file_prefix=None):
    data = numpy.loadtxt('data/ps8/data2', dtype=numpy.float64)
    ms = tispy.lyap_k('-d', 155, '-m', dim, '-M', dim, input=data)
    pargs = cut(ms[:,0], ms[:,1])

    # Find the average slope of the first two points.
    total = 0.0
    count = len(pargs) / 2
    for i in xrange(0, len(pargs), 2):
        [x1, x2] = pargs[i][:2]
        [y1, y2] = pargs[i+1][:2]
        total += (y2-y1) / (0.31*(x2-x1))

    print 'Found Lyapunov exponent: {0:.6f}'.format(total/count)
    plot.render(
            *pargs, 
            xlabel='Iterations',
            ylabel='Logarithm of the Stretching Factor',
            title='Calculating the Lyapunov Exponent',
            file_prefix=suffixed(file_prefix, '_4')
        )

def pr5b1(dim):
    data = numpy.loadtxt('data/ps8/data2', dtype=numpy.float64)
    ms = tispy.lyap_k('-d', 155, '-m', dim, '-M', dim, input=data)
    pargs = tuple([xs[:11] for xs in cut(ms[:,0], ms[:,1])])

    plot.render(*pargs)

def pr5b2(dim, cutoff):
    data = numpy.loadtxt('data/ps8/data2', dtype=numpy.float64)
    ms = tispy.lyap_k('-d', 155, '-m', dim, '-M', dim, input=data)
    pargs = cut(ms[:,0], ms[:,1])

    total = 0.0
    count = len(pargs) / 2
    for i in xrange(0, len(pargs), 2):
        xs = 0.31*pargs[i][:cutoff]
        ys = pargs[i+1][:cutoff]
        ps = numpy.polyfit(xs, ys, 1)
        total += ps[0]

    print 'Found Lyapunov exponent: {0:.6f}'.format(total/count)

def pr6(file_prefix=None):
    lfunc = lorenz.lorenz(16, 45, 4)
    ts, vs = rungekutta.rk4(
                        lfunc, 
                        0.0, 
                        numpy.array([-13.0, -12.0, 52.0], dtype=numpy.float64), 
                        0.001, 
                        30000
                    )
    xs = vs.transpose()[:,0]
    data = numpy.array(zip(xs, ts), dtype=numpy.float64)
    ms = tispy.mutual('-D', 1600, input=data)
    tau = first_min(ms)
    ws = tispy.delay('-d', int(tau), '-m', 7, input=data)
    col1 = 0
    col2 = 5
    plot.render(
                ws[:,col1], 
                ws[:,col2], 
                'k.', 
                markersize=0.6,
                title=r'Delay Coordinate Embedding: {0}, $\tau={1}$ s'.format(
                        r'lorenz', 0.001*tau
                    ),
                xlabel=r'$x(t+{0:.3f})$'.format(col1*0.001*tau),
                ylabel=r'$x(t+{0:.3f})$'.format(col2*0.001*tau),
                file_prefix=suffixed(file_prefix, '_6')
            )
    return tau

def pr6x1(tau, file_prefix=None):
    lfunc = lorenz.lorenz(16, 45, 4)
    ts, vs = rungekutta.rk4(
                        lfunc, 
                        0.0, 
                        numpy.array([-13.0, -12.0, 52.0], dtype=numpy.float64), 
                        0.001, 
                        30000
                    )
    xs = vs.transpose()[:,0]
    data = numpy.array(zip(xs, ts), dtype=numpy.float64)
    ms = tispy.lyap_k('-d', int(tau), '-m', 7, '-M', 7, input=data)
    pargs = cut(ms[:,0], ms[:,1])

    total = 0.0
    count = len(pargs) / 2
    for i in xrange(0, len(pargs), 2):
        xs = 0.31*pargs[i][:50]
        ys = pargs[i+1][:50]
        ps = numpy.polyfit(xs, ys, 1)
        total += ps[0]
    print 'Lorenz lyapunov exponent: {0}'.format(total/count)

    plot.render(
            *pargs,
            xlabel='Iterations',
            ylabel='Logarithm of the Stretching Factor',
            title='Calculating the Lyapunov Exponent',
            file_prefix=suffixed(file_prefix, '_7')
        )    

def pr6x2():
    vfunc = variational(16, 45, 4)
    x0 = ic(-13.0, -12.0, 52.0)
    ts, xs = rungekutta.rk4(vfunc, 0.0, x0, 0.001, 30000)
    ms = numpy.reshape(xs[3:,-1], (3,3))
    ws, vs = eig(ms)
    return [numpy.log(numpy.abs(w))/30000 for w in ws]

def main(argv=None):
    if argv is None:
        argv = sys.argv

    file_prefix = None
    delay = 160

    try:
        options, args = getopt.getopt(argv[1:], 'f:D:')
        for opt, arg in options:
            if opt == '-f':
                file_prefix = arg 
            if opt == '-D':
                delay = int(arg)
    except getopt.GetoptError as err:
        print str(err)
        return 2

    pr2(delay=delay, file_prefix=file_prefix)
    pr3(file_prefix=file_prefix)
    pr4(file_prefix=file_prefix)
    pr5(file_prefix=file_prefix)
    tau = pr6(file_prefix=file_prefix)
    pr6x1(tau, file_prefix=file_prefix)
    print pr6x2()

    return 0

if __name__ == "__main__":
    sys.exit(main())