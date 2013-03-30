###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
# File: ps10.py
# Author: Ken Sheedlo
#
# Leap-Nanosecond Observation Prediction
#
###############################################################################

from __future__ import division

import dimension
import getopt
import lorenz
import numpy
import plot
import rungekutta
import sys
import tispy

from ps9 import first_min
from utils import suffixed, mod2pi

def find_loglog_slope(xs, x0, file_prefix=None):
    epss = numpy.array([(2 ** x) for x in xrange(10, -18, -1)], dtype=numpy.float64)
    ds = dimension.capacity(xs, x0, epss)
    plot.loglog(ds[:,0], ds[:,1])
    lbound = numpy.float64(raw_input('Choose a lower bound: '))
    ubound = numpy.float64(raw_input('Choose an upper bound: '))
    iss = [i for (i, d) in enumerate(ds[:,0]) if lbound <= d and d <= ubound]
    i_low = iss[0]
    i_hi = iss[-1] + 1
    ds_eslice = numpy.log(ds[i_low:i_hi,0])
    ds_nslice = numpy.log(ds[i_low:i_hi,1])
    ps = numpy.polyfit(ds_eslice, ds_nslice, 1)

    def _render(axes):
        axes.loglog(ds[:,0], ds[:,1])
        axes.loglog([lbound, lbound], axes.get_ybound(), 'k')
        axes.loglog([ubound, ubound], axes.get_ybound(), '#414243')
        (lne, hne) = axes.get_ybound()
        lx = ((numpy.e ** (-ps[1])) * lne) ** (1/ps[0])
        hx = ((numpy.e ** (-ps[1])) * hne) ** (1/ps[0])
        axes.loglog([lx, hx], [lne, hne], 'k--')
        axes.legend((
                    r'$N(\varepsilon)$', 
                    'Lower scaling bound', 
                    'Upper scaling bound', 
                    'Linear fit'
                ), loc=4)

    plot.render(
                title=r'Capacity Dimension $D_c = {0}$'.format(ps[0]), 
                xlabel=r'$\frac{1}{\varepsilon}$',
                ylabel=r'$N(\varepsilon)$',
                ax_callback=_render, 
                file_prefix=file_prefix
            )
    return ps[0]

def pr2a(file_prefix=None):
    lfunc = lorenz.lorenz(16, 45, 4)
    ts, xxs = rungekutta.rk4(
                            lfunc, 
                            0.0, 
                            numpy.array([-13.0, -12.0, 52.0], dtype=numpy.float64), 
                            0.0001, 
                            300000
                        )
    xs = xxs.transpose()[:,0]
    data = numpy.array(zip(xs, ts), dtype=numpy.float64)
    ms = tispy.mutual('-D', 16000, input=data)
    tau = first_min(ms)
    ws = tispy.delay('-d', int(tau), '-m', 7, input=data)
    x0 = numpy.array([-35, -35], dtype=numpy.float64)
    zs = numpy.array(zip(ws[100000:,0], ws[100000:,5]), dtype=numpy.float64)
    d_cap = find_loglog_slope(zs, x0, file_prefix=suffixed(file_prefix, '_2a'))
    print 'Lorenz d_cap = {0:.6f}'.format(d_cap)

def pr2b(file_prefix=None):
    data = numpy.loadtxt('data/ps8/data2.first250sec', dtype=numpy.float64)
    vs = tispy.delay('-d', 155, '-m', 8, input=data)
    xs = numpy.array(zip([mod2pi(v) for v in vs[:,0]], [mod2pi(v) for v in vs[:,2]]), 
            dtype=numpy.float64)
    x0 = numpy.array([0] * 2, dtype=numpy.float64)
    d_cap = find_loglog_slope(xs, x0, file_prefix=suffixed(file_prefix, '_2b'))
    print 'd_cap = {0:.6f}'.format(d_cap)

def pr2c(file_prefix=None):
    data = numpy.loadtxt('data/ps8/data2', dtype=numpy.float64)
    vs = tispy.delay('-d', 155, '-m', 8, input=data)
    xs = numpy.array(zip([mod2pi(v) for v in vs[:,0]], [mod2pi(v) for v in vs[:,2]]), 
            dtype=numpy.float64)
    x0 = numpy.array([0] * 2, dtype=numpy.float64)
    d_cap = find_loglog_slope(xs, x0, file_prefix=suffixed(file_prefix, '_2c'))
    print 'd_cap = {0:.6f}'.format(d_cap)

def extrema():
    lfunc = lorenz.lorenz(16, 45, 4)
    ts, xxs = rungekutta.rk4(
                            lfunc, 
                            0.0, 
                            numpy.array([-13.0, -12.0, 52.0], dtype=numpy.float64), 
                            0.0001, 
                            300000
                        )
    xs = xxs.transpose()[:,0]
    data = numpy.array(zip(xs, ts), dtype=numpy.float64)
    ms = tispy.mutual('-D', 16000, input=data)
    tau = first_min(ms)
    print 'Tau: {0:.6f}'.format(tau)
    ws = tispy.delay('-d', int(tau), '-m', 7, input=data)
    zs = ws[100000:,:]
    mins = numpy.empty(7, dtype=numpy.float64)
    maxs = numpy.empty(7, dtype=numpy.float64)
    for i in xrange(7):
        mins[i] = min(zs[:,i])
        maxs[i] = max(zs[:,i])
    print 'Mins: {0}'.format(mins)
    print 'Maxs: {0}'.format(maxs)

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

    # pr2a(file_prefix=file_prefix)
    pr2b(file_prefix=file_prefix)
    pr2c(file_prefix=file_prefix)

    return 0

if __name__ == "__main__":
    sys.exit(main())