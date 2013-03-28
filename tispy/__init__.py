###############################################################################
#
# File: tispy/__init__.py
# Author: Ken Sheedlo
#
# TISEAN interface library for Python
#
###############################################################################

import sys
import wrapper

PROGRAMS = [
    'ar-model',
    'arima-model',
    'av-d2',
    'corr',
    # 'd2',     # d2 intentionally left out due to currently incompatible file
                # structure.
    'delay',
    'extrema',
    'false_nearest',
    'fsle',
    # 'ghkss', # Incompatible file structure.
    'histogram',
    'lfo-ar',
    'lfo-run',
    'lfo-test',
    'low121',
    'lyap_spec',
    'lzo-gm',
    'lzo-run',
    'lzo-test',
    'makenoise',
    'mem_spec',
    'mutual',
    # 'nrlazy', # Incompatible file structure.
    'nstat_z',
    'pca',
    'poincare',
    'polyback',
    'polynomp',
    'rbf',
    'recurr',
    'resample',
    'rescale',
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

FILE_OUTPUT_REQUIRED = [
    'boxcount',
    'lyap_k',
    'lyap_r',
    'polynom',
    'polypar',
]

selfmod = sys.modules[__name__]
selfmod.__dict__.update([wrapper.activate(program) for program in PROGRAMS])
selfmod.__dict__.update([
                    wrapper.activate(program, output_to_file=True) 
                    for program in FILE_OUTPUT_REQUIRED
                ])
