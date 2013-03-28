###############################################################################
#
# File: test.py
# Author: Ken Sheedlo
#
# TISEAN interface library for Python, unit tests.
#
###############################################################################

import numpy
import wrapper
import unittest

class TestTispy(unittest.TestCase):
    '''
    Test suite for tispy library.

    '''
    def test_mutual_should_construct_mutual_information(self):
        '''
        Tests the mutual program to make sure it is working.

        '''
        data = numpy.loadtxt('test.dat')
        (_, mutual) = wrapper.activate('mutual')
        muts = mutual(input=data)
        expected = numpy.array([
                            [ 0., 2.766932],
                            [ 1., 2.626527],
                            [ 2., 2.523629],
                            [ 3., 2.43525 ],
                            [ 4., 2.356612],
                            [ 5., 2.28539 ],
                            [ 6., 2.220294],
                            [ 7., 2.160475],
                            [ 8., 2.105323],
                            [ 9., 2.054395],
                            [10., 2.007321],
                            [11., 1.963788],
                            [12., 1.923651],
                            [13., 1.886742],
                            [14., 1.852874],
                            [15., 1.821637],
                            [16., 1.792148],
                            [17., 1.763563],
                            [18., 1.734117],
                            [19., 1.704597],
                            [20., 1.673778]
                        ], dtype=numpy.float64)
        self.assertEquals(muts.shape, expected.shape)
        for i in xrange(21):
            self.assertAlmostEqual(expected[i, 0], muts[i, 0])
            self.assertAlmostEqual(expected[i, 1], muts[i, 1])

if __name__ == "__main__":
    unittest.main()