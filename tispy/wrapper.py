###############################################################################
#
# File: tispy/wrapper.py
# Author: Ken Sheedlo
#
# TISEAN interface library for Python
#
###############################################################################

import numpy
import os
import StringIO
import subprocess
import tempfile
import uuid

def activate(program, output_to_file=False):
    '''
    Constructs a callback interface to a TISEAN program.

    Params:
        program     The name of the TISEAN program to call.

    Returns: a tuple (name, callback) where
        name        A suitable Python name for the program. This will be equal
                    to the TISEAN program's name unless it uses Python special
                    characters (e.g., -). In this case an appropriate substitute
                    will be used (- => _).
        callback    The function to run, conforming to the standard tispy 
                    interface. It takes an optional input keyword-arg that will
                    be converted to a string and passed to TISEAN as standard 
                    input. It returns the result from TISEAN as a Numpy ndarray.
    '''
    pyname = program.replace('-', '_')
    tempdir = tempfile.gettempdir()

    def _straightline(dargs):
        '''
        Converts a keyword-arg dictionary into a shell arguments.

        '''
        def _combine(lst, kv):
            return lst + ['-{0}'.format(kv[0]), str(kv[1])]
        return reduce(_combine, dargs.items(), [])

    def _callback(*args, **kwargs):
        '''
        Standard tispy library interface callback.

        '''
        iarray = kwargs.get('input')
        idata = None
        output_name = None
        seq_args = [str(arg) for arg in args]

        if output_to_file:
            output_name = tempdir + str(uuid.uuid4())
            seq_args += ['-o', output_name]

        if iarray is not None:
            ibuf = StringIO.StringIO()
            numpy.savetxt(ibuf, iarray)
            idata = ibuf.getvalue()
            ibuf.close()

        pargs = [program, '-V', '0'] + list(seq_args) + _straightline(dict({
                        kv for kv in kwargs.items()
                        if kv[0] != 'input'
                    }))
        child = subprocess.Popen(
                            pargs, 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                        )
        (outdata, _) = child.communicate(input=idata)

        buf = open(output_name, 'r') if output_to_file else StringIO.StringIO(outdata)
        try:
            return numpy.loadtxt(buf)
        finally:
            buf.close()
            if output_to_file:
                os.remove(output_name)

    return (pyname, _callback)
