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