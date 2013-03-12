###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: utils.py
# Author: Ken Sheedlo
#
# Generic utility functions.
#
###############################################################################

'''
Generic utility library for chaos assignments.

'''

import numpy

from constants import EPSILON

def split_dict(keys, dict_elt):
    '''
    Splits a dictionary into two using the specified key set.

    '''
    key_set = set(keys)
    dict_items = dict_elt.items()
    with_keys = dict([(k, v) for (k, v) in dict_items
                        if k in key_set
                    ])
    without_keys = dict([(k, v) for (k, v) in dict_items
                        if k not in key_set
                    ])
    return with_keys, without_keys

def fp_equal(x1, x2, tol=EPSILON):
    '''
    Determines whether two numbers are equal to within a satisfactory bound.

    '''
    return numpy.abs(x1-x2) < tol

def bind_kwargs(func, **kwargs):
    '''
    Binds the specified kwargs to the specified function.

    '''
    outer_kwargs = dict(kwargs)

    def _bound(*args, **kwargs):
        instance_kwargs = dict(outer_kwargs)
        instance_kwargs.update(kwargs)
        return func(*args, **instance_kwargs)
    return _bound

def ufunc(nin, nout, dtype=object):
    '''
    Wraps numpy.frompyfunc in a decorator.

    '''
    def _decorator(func):
        '''
        Decorates a function, making it a Numpy ufunc.

        '''
        uf = numpy.frompyfunc(func, nin, nout)
        return bind_kwargs(uf, dtype=dtype)
    return _decorator

def mod2pi(theta):
    modulus = int(numpy.floor(theta / (2*numpy.pi)))
    return theta - (modulus*2*numpy.pi)

def suffixed(s, suffix):
    return None if s is None else '{0}{1}'.format(s, suffix)