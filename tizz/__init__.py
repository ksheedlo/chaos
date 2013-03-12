###############################################################################
#
# File: tizz/__init__.py
# Author: Ken Sheedlo
#
# TISEAN interface library for Python
#
###############################################################################

import numpy
import StringIO
import subprocess
import sys

PROGRAMS = [
    'ar-model',
    'arima-model',
    'av-d2',
    'boxcount',
    'causality',
    'changes',
    'corr',
    'd2',
    'delay',
    'extrema',
    'false_nearest',
    'fsle',
    'ghkss',
    'histogram',
    'lfo-ar',
    'lfo-run',
    'lfo-test',
    'low121',
    'lyap_k',
    'lyap_r',
    'lyap_spec',
    'lzo-gm',
    'lzo-run',
    'lzo-test',
    'makenoise',
    'mem_spec',
    'mutual',
    'nrlazy',
    'nstat_z',
    'pca',
    'poincare',
    'polyback',
    'polynom',
    'polynomp',
    'polypar',
    'rand',
    'rbf',
    'recurr',
    'resample',
    'rescale',
    'routines',
    'sav_gol',
    'xcor',
    'xzero',
    'zeroth',
    'addnoise',
    'ar-run',
    'autocor',
    'c1',
    'c2d',
    'c2g',
    'c2naive',
    'c2t',
    'changes',
    'choose',
    'cluster',
    'compare',
    'delay',
    'endtoend',
    'events',
    'henon',
    'ikeda',
    'intervals',
    'lazy',
    'lorenz',
    'notch',
    'pc',
    'predict',
    'project',
    'randomize',
    'randomize_auto',
    'randomize_cool',
    'randomize_cost',
    'randomize_extend',
    'randomize_perm',
    'randomize_spike',
    'randomize_uneven',
    'rms',
    'spectrum',
    'spikeauto',
    'spikespec',
    'stp',
    'surrogates',
    'timerev',
    'upo',
    'upoembed',
    'wiener',
    'xc2',
    'xrecur'
]

def _activate(program):
    '''
    Constructs a callback interface to a TISEAN program.

    Params:
        program     The name of the TISEAN program to call.

    Returns: a tuple (name, callback) where
        name        A suitable Python name for the program. This will be equal
                    to the TISEAN program's name unless it uses Python special
                    characters (e.g., -). In this case an appropriate substitute
                    will be used (- => _).
        callback    The function to run, conforming to the standard tizz 
                    interface. It takes an optional input keyword-arg that will
                    be converted to a string and passed to TISEAN as standard 
                    input. It returns the result from TISEAN as a Numpy ndarray.
    '''
    pyname = program.replace('-', '_')

    def _straightline(dargs):
        '''
        Converts a keyword-arg dictionary into a shell arguments.

        '''
        def _combine(lst, kv):
            return lst + ['-{0}'.format(kv[0]), str(kv[1])]
        return reduce(_combine, dargs.items(), [])

    def _callback(*args, **kwargs):
        '''
        Standard tizz library interface callback.

        '''
        iarray = kwargs.get('input')
        idata = None

        if iarray is not None:
            ibuf = StringIO.StringIO()
            numpy.savetxt(ibuf, iarray)
            idata = ibuf.getvalue()
            ibuf.close()

        pargs = [program, '-V', '0'] + list(args) + _straightline(dict({
                        kv for kv in kwargs.items()
                        if kv[0] != 'input'
                    }))
        child = subprocess.Popen(
                            pargs, 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE
                        )
        (outdata, errdata) = child.communicate(input=idata)

        if errdata:
            print >> sys.stderr, errdata

        buf = StringIO.StringIO(outdata)
        try:
            return numpy.loadtxt(buf)
        finally:
            buf.close()

    return (pyname, _callback)

selfmod = sys.modules[__name__]
for program in PROGRAMS:
    (pname, callback) = _activate(program)
    selfmod.__dict__[pname] = callback
