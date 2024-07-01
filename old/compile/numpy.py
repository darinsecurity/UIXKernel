import os
import sys
import types

PINLINED_DEFAULT_PACKAGE = 'numpy'
PINLINER_MODULE_NAME = 'pinliner_loader'
loader_version = '0.2.1'

FORCE_EXC_HOOK = None

inliner_importer_code = '''
import imp
import marshal
import os
import struct
import sys
import types


class InlinerImporter(object):
    version = '%(loader_version)s'
    def __init__(self, data, datafile, set_excepthook=True):
        self.data = data
        self.datafile = datafile
        if set_excepthook:
            sys.excepthook = self.excepthook

    @staticmethod
    def excepthook(type, value, traceback):
        import traceback as tb
        tb.print_exception(type, value, traceback)

    def find_module(self, fullname, path):
        module = fullname in self.data
        if module:
            return self

    def get_source(self, fullname):
        __, start, end, ts = self.data[fullname]
        with open(self.datafile) as datafile:
            datafile.seek(start)
            code = datafile.read(end - start)
        return code

    def get_code(self, fullname, filename):
        py_ts = self.data[fullname][3]
        try:
            with open(fullname + '.pyc', 'rb') as pyc:
                pyc_magic = pyc.read(4)
                pyc_ts = struct.unpack('<I', pyc.read(4))[0]
                if pyc_magic == imp.get_magic() and pyc_ts == py_ts:
                    return marshal.load(pyc)
        except:
            pass

        code = self.get_source(fullname)
        compiled_code = compile(code, filename, 'exec')

        try:
            with open(fullname + '.pyc', 'wb') as pyc:
                pyc.write(imp.get_magic())
                pyc.write(struct.pack('<I', py_ts))
                marshal.dump(compiled_code, pyc)
        except:
            pass
        return compiled_code

    def load_module(self, fullname):
        # If the module it's already in there we'll reload but won't remove the
        # entry if we fail
        exists = fullname in sys.modules

        module = types.ModuleType(fullname)
        module.__loader__ = self

        is_package = self.data[fullname][0]
        path = fullname.replace('.', os.path.sep)
        if is_package:
            module.__package__ = fullname
            module.__file__ = os.path.join(path, '__init__.py')
            module.__path__ = [path]
        else:
            module.__package__ = fullname.rsplit('.', 1)[0]
            module.__file__ = path + '.py'

        sys.modules[fullname] = module

        try:
            compiled_code = self.get_code(fullname, module.__file__)
            exec(compiled_code, module.__dict__)
        except:
            if not exists:
                del sys.modules[fullname]
            raise

        return module
''' % {'loader_version': loader_version}

'''

import unittest
import pytest

try:
    import tinynumpy.tinynumpy as tinynumpy
except ImportError:
    import tinynumpy as tinynumpy

# Numpy is optional. If not available, will compare against ourselves.
try:
    import numpy
except ImportError:
    numpy = tinynumpy

#numpy.set_printoptions(formatter={'float': repr})

def _clean_repr(a):
    return "".join(repr(a).split())

class TestNDArray(unittest.TestCase):
    def setUp(self):
        a = [[ 1.0, 2.0, 3.0, 4.0],
             [ 5.0, 6.0, 7.0, 8.0],
             [ 9.0,10.0,11.0,12.0],
             [13.0,14.0,15.0,16.0]]
        self.t0 = tinynumpy.array(a)
        self.n0 = numpy.array(a)

    def test_repr(self):
        self.assertEqual(_clean_repr(self.t0), _clean_repr(self.n0))

    def test_index(self):
        self.assertEqual(float(self.t0[1,1]), float(self.n0[1,1]))

    def test_slice(self):
        self.assertEqual(_clean_repr(self.t0[1:]), _clean_repr(self.n0[1:]))
        self.assertEqual(_clean_repr(self.t0[1:,1:]), _clean_repr(self.n0[1:,1:]))
        self.assertEqual(_clean_repr(self.t0[-1:,]), _clean_repr(self.n0[-1:,]))
        self.assertEqual(_clean_repr(self.t0[-1:,1]), _clean_repr(self.n0[-1:,1]))

    def test_double_slice(self):
        self.assertEqual(_clean_repr(self.t0[1:][2::2]), _clean_repr(self.n0[1:][2::2]))

    def test_len(self):
        self.assertEqual(len(self.t0), len(self.n0))

    def test_newaxis(self):
        self.assertEqual(self.t0[tinynumpy.newaxis,2:].shape, (1,2,4))
        self.assertEqual(self.n0[numpy.newaxis,2:].shape, (1,2,4))
        self.assertEqual(_clean_repr(self.t0[tinynumpy.newaxis,2:]), _clean_repr(self.n0[numpy.newaxis,2:]))

class TestNDIter(unittest.TestCase):
    def setUp(self):
        self.t0 = tinynumpy.array([[1.0,2.0],[3.0,4.0]])
        self.n0 = numpy.array([[1.0,2.0],[3.0,4.0]])

    def test_basic(self):
        self.assertEqual(
            [float(i) for i in tinynumpy.nditer(self.t0)],
            [float(i) for i in numpy.nditer(self.n0)])

    def test_reversed(self):
        # NumPy reversed just returns array(1.0).
        self.assertEqual(
            [float(i) for i in reversed(tinynumpy.nditer(self.t0))], 
            [4.0, 3.0, 2.0, 1.0])

class TestFunctions(unittest.TestCase):
    def setUp(self):
        a0 = [
                [
                    [
                        1, 
                        [1, 1, 1, 1], 
                        [2, 2],
                        [2, 2]
                    ], 
                    1
                ], 
                [2, 2, 1, 1], 
                [3, 3],
                [3, 3]
            ]
        self.t0 = tinynumpy.array(a0)

        a1 = [[1,2],[3,4]]
        self.t1 = tinynumpy.array(a1)
        self.n1 = numpy.array(a1)

    def test_array(self):
        # NumPy requires that the input array be full in all dimensions, so don't check compatibility.
        self.assertEqual(self.t0.shape, (4, 4, 4, 4))

    def test_zeros(self):
        self.assertEqual(tinynumpy.zeros((5,5,5)).sum(), 0)

    def test_eye(self):
        self.assertEqual(_clean_repr(tinynumpy.eye(3)), _clean_repr(numpy.eye(3)))
        self.assertEqual(tinynumpy.eye(25).sum(), 25)

    def test_sum(self):
        self.assertEqual(self.t1.sum(), 10)

    def test_mean(self):
        self.assertEqual(tinynumpy.array([-5, 5]).mean(), 0)

    def test_argmax(self):
        self.assertEqual(tinynumpy.array([1, 2, 3]).argmax(), 2)

    def test_argmin(self):
        self.assertEqual(tinynumpy.array([1, 2, -3]).argmin(), 2)

    def test_cumsum(self):
        self.assertEqual(_clean_repr(tinynumpy.array([1, 2, 3]).cumsum()), _clean_repr(tinynumpy.array([1, 3, 6])))

    def test_cumprod(self):
        self.assertEqual(_clean_repr(tinynumpy.array([1, 2, 3]).cumprod()), _clean_repr(tinynumpy.array([1, 2, 6])))

    def test_all(self):
        self.assertEqual(tinynumpy.array([1, 0, 1]).all(), False)

    def test_any(self):
        self.assertEqual(tinynumpy.array([1, 0, 1]).any(), True)

    def test_argmin(self):
        self.assertEqual(tinynumpy.array([1, 2, -3]).argmin(), 2)

    def test_sum(self):
        self.assertEqual(tinynumpy.array([1, 2, -3]).sum(), 0)

    def test_max(self):
        self.assertEqual(self.t1.max(), 4)

    def test_min(self):
        self.assertEqual(self.t1.min(), 1)

    def test_prod(self):
        self.assertEqual(tinynumpy.array([1, 2, 3, 10]).prod(), 60)

    def test_ptp(self):
        self.assertEqual(tinynumpy.array([-1, 2, 3]).ptp(), 4)

    def test_fill(self):
        t = tinynumpy.zeros((4, 4, 4))
        t.fill(1)
        self.assertEqual(t.sum(), 4*4*4)

    def test_copy(self):
        t = self.t1.copy()
        t[0,0] = 0
        self.assertEqual(self.t1.sum(), 10)
        self.assertEqual(t.sum(), 9)

    def test_flatten(self):
        self.assertEqual(_clean_repr(self.t1.flatten()), _clean_repr(tinynumpy.array([1, 2, 3, 4])))

    def test_var(self):
        self.assertEqual(tinynumpy.array([1,1,1,1]).var(), 0)
        self.assertEqual(_clean_repr(self.t1.var()), _clean_repr(self.n1.var()))

    def test_std(self):
        self.assertEqual(tinynumpy.array([1,1,1,1]).std(), 0)
        self.assertEqual(int(self.t1.std()*1000000), int(self.n1.std()*1000000))

if __name__ == '__main__':
    unittest.main()
    #unittest.main(defaultTest='TestNDArray.test_newaxis')# -*- coding: utf-8 -*-
# Copyright (c) 2014, Almar Klein and Wade Brainerd
# tinynumpy is distributed under the terms of the MIT License.

""" Test suite for tinynumpy
"""

import os
import sys
import ctypes

import pytest
from _pytest import runner
from pytest import raises, skip

try:
    import tinynumpy.tinynumpy as tnp
except ImportError:
    import tinynumpy as tnp

# Numpy is optional. If not available, will compare against ourselves.
try:
    import numpy as np
except ImportError:
    np = tnp


def test_TESTING_WITH_NUMPY():
    # So we can see in the result whether numpy was used
    if np is None or np is tnp:
        skip('Numpy is not available')


def test_shapes_and_strides():
    
    for shape in [(9, ), (109, ), 
                  (9, 4), (109, 104), 
                  (9, 4, 5), (109, 104, 105),
                  (9, 4, 5, 6),  # not (109, 104, 105, 106) -> too big
                  ]:
        
        # Test shape and strides
        a = np.empty(shape)
        b = tnp.empty(shape)
        assert a.ndim == len(shape)
        assert a.ndim == b.ndim
        assert a.shape == b.shape
        assert a.strides == b.strides
        assert a.size == b.size
        
        # Also test repr length
        if b.size > 100:
            assert len(repr(b)) < 80
        else:
            assert len(repr(b)) > (b.size * 3)  # "x.0" for each element


def test_repr():
    
    for dtype in ['float32', 'float64', 'int32', 'int64']:
        for data in [[1, 2, 3, 4, 5, 6, 7, 8],
                    [[1, 2], [3, 4], [5, 6], [7, 8]],
                    [[[1, 2], [3, 4]],[[5, 6], [7, 8]]],
                    ]:
            a = np.array(data, dtype)
            b = tnp.array(data, dtype)
            # Compare line by line (forget leading whitespace)
            charscompared = 0
            for l1, l2 in zip(repr(a).splitlines(), repr(b).splitlines()):
                l1, l2 = l1.rstrip(), l2.rstrip()
                l1, l2 = l1.split('dtype=')[0], l2.split('dtype=')[0]
                assert l1 == l2
                charscompared += len(l1)
            assert charscompared > (3 * b.size)


def test_dtype():
    
    for shape in [(9, ), (9, 4), (9, 4, 5)]:
        for dtype in ['bool', 'int8', 'uint8', 'int16', 'uint16',
                      'int32', 'uint32', 'float32', 'float64']:
            a = np.empty(shape, dtype=dtype)
            b = tnp.empty(shape, dtype=dtype)
            assert a.shape == b.shape
            assert a.dtype == b.dtype
            assert a.itemsize == b.itemsize
    
    raises(TypeError, tnp.zeros, (9, ), 'blaa')
    
    assert tnp.array([1.0, 2.0]).dtype == 'float64'
    assert tnp.array([1, 2]).dtype == 'int64'


def test_reshape():
    
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype='int32')
    b = tnp.array([1, 2, 3, 4, 5, 6, 7, 8], dtype='int32')
    
    for shape in [(2, 4), (4, 2), (2, 2, 2), (8,)]:
        a.shape = shape
        b.shape = shape
        assert a.shape == b.shape
        print(repr(a), repr(b), a.strides, b.strides)
        assert a.strides == b.strides
    
    a.shape = 2, 4
    b.shape = 2, 4
    
    # Test transpose
    assert b.T.shape == (4, 2)
    assert (a.T == b.T).all()
    assert (b.T.T == b).all()
    
    # Make non-contiguous versions
    a2 = a[:, 2:]
    b2 = b[:, 2:]
    
    # Test contiguous flag
    assert a.flags['C_CONTIGUOUS']
    assert not a2.flags['C_CONTIGUOUS']
    
    # Test base
    assert a2.base is a
    assert b2.base is b
    assert a2[:].base is a
    assert b2[:].base is b
    
    # Fail
    with raises(ValueError):  # Invalid shape
        a.shape = (3, 3)
    with raises(ValueError):
        b.shape = (3, 3)
    with raises(AttributeError):  # Cannot reshape non-contiguous arrays
        a2.shape = 4,
    with raises(AttributeError):
        b2.shape = 4,


def test_from_and_to_numpy():
    # This also tests __array_interface__
    
    for dtype in ['float32', 'float64', 'int32', 'uint32', 'uint8', 'int8']:
        for data in [[1, 2, 3, 4, 5, 6, 7, 8],
                    [[1, 2], [3, 4], [5, 6], [7, 8]],
                    [[[1, 2], [3, 4]],[[5, 6], [7, 8]]],
                    ]:
                        
            # Convert from numpy, from tinynumpy, to numpy
            a1 = np.array(data, dtype)
            b1 = tnp.array(a1)
            b2 = tnp.array(b1)
            a2 = np.array(b2)
            
            # Check if its the same
            for c in [b1, b2, a2]:
                assert a1.shape == c.shape
                assert a1.dtype == c.dtype
                assert a1.strides == c.strides
                assert (a1 == c).all()
    
    # Also test using a numpy array as a buffer
    a = np.array([[1, 2], [3, 4], [5, 6], [7, 8]], 'float32')
    b = tnp.ndarray(a.shape, a.dtype, strides=a.strides, buffer=a.ravel())
    assert (a==b).all()
    
    # Test that is indeed same data
    a[0, 0] = 99
    assert (a==b).all()


def test_from_ctypes():
    
    for type, dtype in [(ctypes.c_int16, 'int16'), 
                        (ctypes.c_uint8, 'uint8'), 
                        (ctypes.c_float, 'float32'), 
                        (ctypes.c_double, 'float64')]:
        # Create ctypes array, possibly something that we get from a c lib
        buffer = (type*100)()
        
        # Create array!
        b = tnp.ndarray((4, 25), dtype, buffer=buffer)
        
        # Check that we can turn it into a numpy array
        a = np.array(b, copy=False)
        assert (a == b).all()
        assert a.dtype == dtype
        
        # Verify that both point to the same data
        assert a.__array_interface__['data'][0] == ctypes.addressof(buffer)
        assert b.__array_interface__['data'][0] == ctypes.addressof(buffer)
        
        # also verify offset in __array_interface__ here
        for a0, b0 in zip([a[2:], a[:, 10::2], a[1::2, 10:20:2]],
                          [b[2:], b[:, 10::2], b[1::2, 10:20:2]]):
            pa = a0.__array_interface__['data'][0]
            pb = b0.__array_interface__['data'][0]
            assert pa > ctypes.addressof(buffer)
            assert pa == pb


def test_from_bytes():
    skip('Need ndarray.frombytes or something')
    # Create bytes
    buffer = b'x' * 100
    
    # Create array!
    b = tnp.ndarray((4, 25), 'uint8', buffer=buffer)
    ptr = ctypes.cast(buffer, ctypes.c_void_p).value
    
    # Check that we can turn it into a numpy array
    a = np.array(b, copy=False)
    assert (a == b).all()
    
    # Verify readonly
    with raises(Exception):
        a[0, 0] = 1  
    with raises(Exception):
        b[0, 0] = 1  
    
    # Verify that both point to the same data
    assert a.__array_interface__['data'][0] == ptr
    assert b.__array_interface__['data'][0] == ptr
    
    # also verify offset in __array_interface__ here
    for a0, b0 in zip([a[2:], a[:, 10::2], a[1::2, 10:20:2]],
                        [b[2:], b[:, 10::2], b[1::2, 10:20:2]]):
        pa = a0.__array_interface__['data'][0]
        pb = b0.__array_interface__['data'][0]
        assert pa > ptr
        assert pa == pb


def test_creating_functions():
    
    # Test array
    b1 = tnp.array([[1, 2, 3], [4, 5, 6]])
    assert b1.shape == (2, 3)
    

def test_getitem():
     
    a = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    b = tnp.array([[1, 2, 3, 4], [5, 6, 7, 8]])


# Start vector cross product tests
def test_cross():
    """test the cross product of two 3 dimensional vectors"""

    # Vector cross-product.
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = tnp.cross(x, y)

    assert z == [-3, 6, -3]


def test_2dim_cross():
    """test the cross product of two 2 dimensional vectors"""

    # 2 dim cross-product.
    x = [1, 2]
    y = [4, 5]
    z = tnp.cross(x, y)

    assert z == [-3]


def test_4dim_cross():
    """test the cross product of two 2 dimensional vectors"""

    # 4 dim cross-product.
    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]

    with pytest.raises(IndexError) as execinfo:
        z = tnp.cross(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


def test_mdim_cross():
    """test the cross product of two 4 dimensional vectors"""

    # Mixed dim cross-product.
    x = [1, 2, 3]
    y = [4, 5, 6, 7]

    with pytest.raises(IndexError) as execinfo:
        z = tnp.cross(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


# Start vector dot product tests
def test_dot():
    """test the dot product of two mixed dimensional vectors"""

    # Vector dot-product.
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = tnp.dot(x, y)

    assert z == 32


def test_2dim_dot():
    """test the dot product of two 2 dimensional vectors"""

    # 2 dim dot-product.
    x = [1, 2]
    y = [4, 5]
    z = tnp.dot(x, y)

    assert z == 14


def test_4dim_dot():
    """test the dot product of two 4 dimensional vectors"""

    # 4 dim dot-product.
    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]
    z = tnp.dot(x, y)

    assert z == 70


def test_mdim_dot():
    """test the dot product of two mixed dimensional vectors"""

    # Mixed dim dot-product.
    x = [1, 2, 3]
    y = [4, 5, 6, 7]

    with pytest.raises(IndexError) as execinfo:
        z = tnp.dot(x, y)

    assert 'Vector has invalid dimensions' in str(execinfo.value)


# Start vector determinant tests
def test_det():
    """test calculation of the determinant of a three dimensional"""

    # Three dim determinant
    x = [5, -2, 1]
    y = [0, 3, -1]
    z = [2, 0, 7]
    mat = [x, y, z]

    a = tnp.linalg.det(mat)

    assert a == 103

# Start simple math function tests
def test_add():
    """test the addition function for tinynumpy"""

    x = [5, -2, 1]
    y = [0, 3, -1]

    a = tnp.add(x,y)

    assert a == tnp.array([5, 1, 0], dtype='int64')


def test_subtract():
    """test the addition function for tinynumpy"""

    x = [5, -2, 1]
    y = [0, 3, -1]

    a = tnp.add(x,y)

    assert a == tnp.array([5, -5, -2], dtype='int64')


def test_divide():
    """test the addition function for tinynumpy"""

    x = [15, -12, 3]
    y = 3

    a = tnp.divide(x,y)

    assert a == tnp.array([5, -4, 1], dtype='int64')


def test_multiply():
    """test the addition function for tinynumpy"""

    x = [5, -2, 1]
    y = [0, 3, -1]

    a = tnp.multiply(x,y)

    assert a == tnp.array([0, -6, -1], dtype='int64')


if __name__ == '__main__':
    
    # Run tests with or without pytest. Running with pytest creates
    # coverage report, running without allows PM debugging to fix bugs.
    if False:
        del sys.modules['tinynumpy']  # or coverage wont count globals
        pytest.main('-v -x --color=yes --cov tinynumpy --cov-config .coveragerc '
                    '--cov-report html %s' % repr(__file__))
        # Run these lines to open coverage report
        #import webbrowser
        #webbrowser.open_new_tab(os.path.join('htmlcov', 'index.html'))
    
    else:
        # Collect function names
        test_functions = []
        for line in open(__file__, 'rt').readlines():
            if line.startswith('def'):
                name = line[3:].split('(')[0].strip()
                if name.startswith('test_'):
                    test_functions.append(name)
        # Report
        print('Collected %i test functions.' % len(test_functions))
        # Run
        print('\nRunning tests ...\n')
        for name in test_functions:
            print('Running %s ... ' % name)
            func = globals()[name]
            try:
                func()
            except runner.Skipped as err:
                print('SKIP:', err)
            except Exception:
                print('FAIL')
                raise
            else:
                print('OK')
# -*- coding: utf-8 -*-
# Copyright (c) 2014, Almar Klein and Wade Brainerd
# tinynumpy is distributed under the terms of the MIT License.

""" Benchmarks for tinynumpy

Findings:

* A list of floats costs about 33 bytes per float
* A list if ints costs anout 41 bytes per int
* A huge list of ints 0-255, costs about 1 byter per int
* Python list takes about 5-6 times as much memory than array for 64bit 
  data types. Up to 40 times as much for uint8, unless Python can reuse
  values.
* __slots__ help reduce the size of custom classes
* tinynumpy is about 100 times slower than numpy
* using _toflatlist instead of flat taks 50-60% of time (but more memory)

"""

from __future__ import division

import os
import sys
import time
import subprocess

import numpy as np
import tinynumpy as tnp


def _prettymem(n):
    if n > 2**20:
        return '%1.2f MiB' % (n / 2**20)
    elif n > 2**10:
        return '%1.2f KiB' % (n / 2**10)
    else:
        return '%1.0f B' % n

def _prettysec(n):
    if n < 0.0001:
        return '%1.2f us' % (n * 1000000)
    elif n < 0.1:
        return '%1.2f ms' % (n * 1000)
    else:
        return '%1.2f s' % n


code_template = """
import psutil
import os
import random
import numpy as np
import tinynumpy as tnp

N = 100 * 1000
M = 1000 * 1000

class A(object):
    def __init__(self):
        self.foo = 8
        self.bar = 3.3

class B(object):
    __slots__ = ['foo', 'bar']
    def __init__(self):
        self.foo = 8
        self.bar = 3.3

def getmem():
    process = psutil.Process(os.getpid())
    return process.get_memory_info()[0]

M0 = getmem()
%s
M1 = getmem()
print(M1-M0)
"""

def measure_mem(what, code, divide=1):
    
    cmd = [sys.executable, '-c',  code_template % code]
    res = subprocess.check_output(cmd, cwd=os.getcwd()).decode('utf-8')
    m = int(res) / divide
    
    print('Memory for %s:%s%s' % 
          (what, ' '*(22-len(what)), _prettymem(m)))


def measure_speed(what, func, *args, **kwargs):
    
    
    N = 1
    t0 = time.perf_counter()
    func(*args, **kwargs)
    t1 = time.perf_counter()
    while (t1 - t0) < 0.2:
        N *= 10
        t0 = time.perf_counter()
        for i in range(N):
            func(*args, **kwargs)
        t1 = time.perf_counter()
    
    te = t1 - t0
    print('Time for %s:%s%s  (%i iters)' % 
          (what, ' '*(22-len(what)), _prettysec(te/N), N))


if __name__ == '__main__':
    N = 100 * 1000
    M = 1000 * 1000
    
    print('=== MEMORY ====')
    measure_mem('floats 0-M', 'L = [i*1.0 for i in range(N)]', N)
    measure_mem('ints 0-M', 'L = [i for i in range(N)]', N)
    measure_mem('ints 0-255', 'L = [int(random.uniform(0, 255)) for i in range(N)]', N)
    
    measure_mem('regular object', 'L = [A() for i in range(N)]', N)
    measure_mem('object with slots', 'L = [B() for i in range(N)]', N)
    
    measure_mem('    Numpy arr size 1', 'L = [np.ones((1,)) for i in range(N)]', N)
    measure_mem('Tinynumpy arr size 1', 'L = [tnp.ones((1,)) for i in range(N)]', N)
    
    measure_mem('    Numpy arr size M', 'a = np.ones((M,))')
    measure_mem('Tinynumpy arr size M', 'a = tnp.ones((M,))')
    
    print('=== SPEED ====')
    
    a1 = np.ones((100, 100))
    a2 = tnp.ones((100, 100))
    measure_speed('    numpy sum 10k', a1.sum)
    measure_speed('tinynumpy sum 10k', a2.sum)
    measure_speed('    numpy max 10k', a1.max)
    measure_speed('tinynumpy max 10k', a2.max)
    
    a1 = np.ones((1000, 1000))
    a2 = tnp.ones((1000, 1000))
    measure_speed('    numpy sum 1M', a1.sum)
    measure_speed('tinynumpy sum 1M', a2.sum)
    measure_speed('    numpy max 1M', a1.max)
    measure_speed('tinynumpy max 1M', a2.max)
# Copyright (c) 2014 Eric Allen Youngson

"""This module is used to implement native Python functions to replace those
    called from numpy, when not available"""
# Written by Eric Youngson eric@scneco.com / eayoungs@gmail.com
# Succession Ecological Services: Portland, Oregon

class LinAlgError(Exception):
    pass

def det(A):
    if len(A) == 3 and [len(vec)==3 for vec in A]:
        try:
            # http://mathworld.wolfram.com/Determinant.html
            det_A = (A[0][0] * A[1][1] * A[2][2] + A[0][1] * A[1][2] *
                     A[2][0] + A[0][2] * A[1][0] * A[2][1] - (A[0][2] *
                     A[1][1] * A[2][0] + A[0][1] * A[1][0] * A[2][2] +
                     A[0][0] * A[1][2] * A[2][1]))
        except LinAlgError as e:
            det_A = e
    else:
        raise IndexError('Vector has invalid dimensions')
    return det_A
# -*- coding: utf-8 -*-
# Copyright (c) 2014, Almar Klein and Wade Brainerd
# tinynumpy is distributed under the terms of the MIT License.
#
# Original code by Wade Brainerd (https://github.com/wadetb/tinyndarray)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" 
A lightweight, pure Python, numpy compliant ndarray class.

The documenation in this module is rather compact. For details on each
function, see the corresponding documentation at:
http://docs.scipy.org/doc/numpy/reference/index.html Be aware that the
behavior of tinynumpy may deviate in some ways from numpy, or that
certain features may not be supported.
"""

# todo: keep track of readonly better
# todo: mathematical operators
# todo: more methods?
# todo: logspace, meshgrid
# todo: Fortran order?

from __future__ import division
from __future__ import absolute_import

import ctypes

from math import sqrt
from copy import copy, deepcopy
from collections import Iterable
import operator

import tinynumpy.tinylinalg as linalg
from tinynumpy.tinylinalg import LinAlgError as LinAlgError


# Define version numer
__version__ = '0.0.1dev'

# Define dtypes: struct name, short name, numpy name, ctypes type
_dtypes = [('B', 'b1', 'bool', ctypes.c_bool),
           ('b', 'i1', 'int8', ctypes.c_int8),
           ('B', 'u1', 'uint8', ctypes.c_uint8),
           ('h', 'i2', 'int16', ctypes.c_int16),
           ('H', 'u2', 'uint16', ctypes.c_uint16),
           ('i', 'i4', 'int32', ctypes.c_int32),
           ('I', 'u4', 'uint32', ctypes.c_uint32),
           ('q', 'i8', 'int64', ctypes.c_int64),
           ('Q', 'u8', 'uint64', ctypes.c_uint64),
           ('f', 'f4', 'float32', ctypes.c_float),
           ('d', 'f8', 'float64', ctypes.c_double),
           ]

# Inject common dtype names
_known_dtypes = [d[2] for d in _dtypes]
for d in _known_dtypes:
    globals()[d] = d

newaxis = None

nan = float('nan')

def _convert_dtype(dtype, to='numpy'):
    """ Convert dtype, if could not find, pass as it was.
    """
    if dtype is None:
        return dtype
    dtype = str(dtype)
    index = {'array':0, 'short':1, 'numpy':2, 'ctypes':3}[to]
    for dd in _dtypes:
        if dtype in dd:
            return dd[index]
    return dtype  # Otherwise return original


def _ceildiv(a, b):
    return -(-a // b)


def _get_step(view):
    """ Return step to walk over array. If 1, the array is fully
    C-contiguous. If 0, the striding is such that one cannot
    step through the array.
    """
    cont_strides = _strides_for_shape(view.shape, view.itemsize)
    
    step = view.strides[-1] // cont_strides[-1]
    corrected_strides = tuple([i * step for i in cont_strides])
    
    almost_cont = view.strides == corrected_strides
    if almost_cont:
        return step
    else:
        return 0  # not contiguous


def _strides_for_shape(shape, itemsize):
    strides = []
    stride_product = 1
    for s in reversed(shape):
        strides.append(stride_product)
        stride_product *= s
    return tuple([i * itemsize for i in reversed(strides)])


def _size_for_shape(shape):
    stride_product = 1
    for s in shape:
        stride_product *= s
    return stride_product


def squeeze_strides(s):
    """ Pop strides for singular dimensions. """
    return tuple([s[0]] + [s[i] for i in range(1, len(s)) if s[i] != s[i-1]])


def _shape_from_object(obj):
    
    shape = []
    # todo: make more efficient, use len() etc
    def _shape_from_object_r(index, element, axis):
        try:
            for i, e in enumerate(element):
                _shape_from_object_r(i, e, axis+1)
            while len(shape) <= axis:
                shape.append(0)
            l = i + 1
            s = shape[axis]
            if l > s:
                shape[axis] = l
        except TypeError:
            pass

    _shape_from_object_r(0, obj, 0)
    return tuple(shape)


def _assign_from_object(array, obj):
    key = []
    # todo: make more efficient, especially the try-except
    def _assign_from_object_r(element):
        try:
            for i, e in enumerate(element):
                key.append(i)
                _assign_from_object_r(e)
                key.pop()
        except TypeError:
            array[tuple(key)] = element

    _assign_from_object_r(obj)


def _increment_mutable_key(key, shape):
    for axis in reversed(xrange(len(shape))):
        key[axis] += 1
        if key[axis] < shape[axis]:
            return True
        if axis == 0:
            return False
        key[axis] = 0


def _key_for_index(index, shape):
    key = []
    cumshape = [1]
    for i in reversed(shape):
        cumshape.insert(0, cumshape[0] * i)
    for s in cumshape[1:-1]:
        n = index // s
        key.append(n)
        index -= n * s
    key.append(index)
    return tuple(key)


def _zerositer(n):
    for i in xrange(n):
        yield 0



## Public functions


def array(obj, dtype=None, copy=True, order=None):
    """ array(obj, dtype=None, copy=True, order=None)
    
    Create a new array. If obj is an ndarray, and copy=False, a view
    of that array is returned. For details see:
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html
    """
    dtype = _convert_dtype(dtype)
    
    if isinstance(obj, ndarray):
        # From existing array
        a = obj.view()
        if dtype is not None and dtype != a.dtype:
            a = a.astype(dtype)
        elif copy:
            a = a.copy()
        return a
    if hasattr(obj, '__array_interface__'):
        # From something that looks like an array, we can create
        # the ctypes array for this and use that as a buffer
        D = obj.__array_interface__
        # Get dtype
        dtype_orig = _convert_dtype(D['typestr'][1:])
        # Create array
        if D['strides']:
            itemsize = int(D['typestr'][-1])
            bufsize = D['strides'][0] * D['shape'][0] // itemsize
        else:
            bufsize = _size_for_shape(D['shape'])
        
        BufType = (_convert_dtype(dtype_orig, 'ctypes') * bufsize)
        buffer = BufType.from_address(D['data'][0])
        a = ndarray(D['shape'], dtype_orig,
                    buffer=buffer, strides=D['strides'], order=order)
        # Convert or copy?
        if dtype is not None and dtype != dtype_orig:
            a = a.astype(dtype)
        elif copy:
            a = a.copy()
        return a
    else:
        # From some kind of iterable
        shape = _shape_from_object(obj)
        # Try to derive dtype
        if dtype is None:
            el = obj
            while isinstance(el, (tuple, list)) and el:
                el = el[0]
            if isinstance(el, int):
                dtype = 'int64'
        # Create array
        a = ndarray(shape, dtype, order=None)
        _assign_from_object(a, obj)
        return a


def zeros_like(a, dtype=None, order=None):
    """ Return an array of zeros with the same shape and type as a given array.
    """
    dtype = a.dtype if dtype is None else dtype
    return zeros(a.shape, dtype, order)


def ones_like(a, dtype=None, order=None):
    """ Return an array of ones with the same shape and type as a given array.
    """
    dtype = a.dtype if dtype is None else dtype
    return ones(a.shape, dtype, order)


def empty_like(a, dtype=None, order=None):
    """ Return a new array with the same shape and type as a given array.
    """
    dtype = a.dtype if dtype is None else dtype
    return empty(a.shape, dtype, order)


def zeros(shape, dtype=None, order=None):
    """Return a new array of given shape and type, filled with zeros
    """
    return empty(shape, dtype, order)


def ones(shape, dtype=None, order=None):
    """Return a new array of given shape and type, filled with ones
    """
    a = empty(shape, dtype, order)
    a.fill(1)
    return a


def eye(size):
    """Return a new 2d array with given dimensions, filled with ones on the
    diagonal and zeros elsewhere.
    """
    a = zeros((size,size))
    for i in xrange(size):
        a[i,i] = 1
    return a


def empty(shape, dtype=None, order=None):
    """Return a new array of given shape and type, without initializing entries
    """
    return ndarray(shape, dtype, order=order)


def arange(*args, **kwargs):
    """ arange([start,] stop[, step,], dtype=None)

    Return evenly spaced values within a given interval.
    
    Values are generated within the half-open interval ``[start, stop)``
    (in other words, the interval including `start` but excluding `stop`).
    For integer arguments the function is equivalent to the Python built-in
    `range <http://docs.python.org/lib/built-in-funcs.html>`_ function,
    but returns an ndarray rather than a list.

    When using a non-integer step, such as 0.1, the results will often not
    be consistent.  It is better to use ``linspace`` for these cases.
    """
    # Get dtype
    dtype = kwargs.pop('dtype', None)
    if kwargs:
        x = list(kwargs.keys())[0]
        raise TypeError('arange() got an unexpected keyword argument %r' % x)
    # Parse start, stop, step
    if len(args) == 0:
        raise TypeError('Required argument "start" not found')
    elif len(args) == 1:
        start, stop, step = 0, int(args[0]), 1
    elif len(args) == 2:
        start, stop, step = int(args[0]), int(args[1]), 1
    elif len(args) == 3:
        start, stop, step = int(args[0]), int(args[1]), int(args[2])
    else:
        raise TypeError('Too many input arguments')
    # Init
    iter = xrange(start, stop, step)
    a = empty((len(iter),), dtype=dtype)
    a[:] = list(iter)
    return a


def linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None):
    """ linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
    
    Return evenly spaced numbers over a specified interval. Returns num
    evenly spaced samples, calculated over the interval [start, stop].
    The endpoint of the interval can optionally be excluded.
    """
    # Prepare
    start, stop = float(start), float(stop)
    ra = stop - start
    if endpoint:
        step = ra / (num-1)
    else:
        step = ra / num
    # Create
    a = empty((num,), dtype)
    a[:] = [start + i * step for i in xrange(num)]
    # Return
    if retstep:
        return a, step
    else:
        return a

def add(ndarray_vec1, ndarray_vec2):
    c = []
    for a, b in zip(ndarray_vec1, ndarray_vec2):
        c.append(a+b)
    cRay = array(c)
    return cRay

def subtract(ndarray_vec1, ndarray_vec2):
    c = []
    for a, b in zip(ndarray_vec1, ndarray_vec2):
        c.append(a-b)
    cRay = array(c)
    return cRay

def multiply(ndarray_vec1, ndarray_vec2):
    c = []
    for a, b in zip(ndarray_vec1, ndarray_vec2):
        c.append(a*b)
    cRay = array(c)
    return cRay

def divide(ndarray_vec1, integer):
    c = []
    for a in ndarray_vec1:
        c.append(a / integer)
    cRay = array(c)
    return cRay

def cross(u, v):
    """
    Return the cross product of two 2 or 3 dimensional vectors.
    """

    uDim = len(u)
    vDim = len(v)

    uxv = []

    # http://mathworld.wolfram.com/CrossProduct.html
    if uDim == vDim == 2:
        try:
            uxv = [u[0]*v[1]-u[1]*v[0]]            
        except LinAlgError as e:
            uxv = e        
    elif uDim == vDim == 3:
        try:
            for i in range(uDim):
                uxv = [u[1]*v[2]-u[2]*v[1], -(u[0]*v[2]-u[2]*v[0]),
                       u[0]*v[1]-u[1]*v[0]]
        except LinAlgError as e:
            uxv = e
    else:
        raise IndexError('Vector has invalid dimensions')
    return uxv

def dot(u, v):
    """
    Return the dot product of two equal-dimensional vectors.
    """

    uDim = len(u)
    vDim = len(v)

    # http://reference.wolfram.com/language/ref/Dot.html
    if uDim == vDim:
        try:
            u_dot_v = sum(map(operator.mul, u, v))
        except LinAlgError as e:
            u_dot_v = e
    else:
        raise IndexError('Vector has invalid dimensions')
    return u_dot_v

def reshape(X,shape):
    """
    Returns the reshaped image of an ndarray
    """
    assert isinstance(X, ndarray)
    assert isinstance(shape, tuple) or isinstance(shape, list)
    return X.reshape(shape)

## The class

class ndarray(object):
    """ ndarray(shape, dtype='float64', buffer=None, offset=0,
                strides=None, order=None)
    
    Array class similar to numpy's ndarray, implemented in pure Python.
    This class can be distinguished from a real numpy array in that
    the repr always shows the dtype as a string, and for larger arrays
    (more than 100 elements) it shows a short one-line repr.
    
    An array object represents a multidimensional, homogeneous array
    of fixed-size items.  An associated data-type property describes the
    format of each element in the array.
    
    Arrays should be constructed using `array`, `zeros` or `empty` (refer
    to the See Also section below).  The parameters given here refer to
    a low-level method (`ndarray(...)`) for instantiating an array.
    
    Parameters
    ----------
    shape : tuple of ints
        Shape of created array.
    dtype : data-type, optional
        Any object that can be interpreted as a numpy data type.
    buffer : object contaning data, optional
        Used to fill the array with data. If another ndarray is given,
        the underlying data is used. Can also be a ctypes.Array or any
        object that exposes the buffer interface.
    offset : int, optional
        Offset of array data in buffer.
    strides : tuple of ints, optional
        Strides of data in memory.
    order : {'C', 'F'}, optional  NOT SUPPORTED
        Row-major or column-major order.

    Attributes
    ----------
    T : ndarray
        Transpose of the array. In tinynumpy only supported for ndim <= 3.
    data : buffer
        The array's elements, in memory. In tinynumpy this is a ctypes array.
    dtype : str
        Describes the format of the elements in the array. In tinynumpy
        this is a string.
    flags : dict
        Dictionary containing information related to memory use, e.g.,
        'C_CONTIGUOUS', 'OWNDATA', 'WRITEABLE', etc.
    flat : iterator object
        Flattened version of the array as an iterator. In tinynumpy
        the iterator cannot be indexed.
    size : int
        Number of elements in the array.
    itemsize : int
        The memory use of each array element in bytes.
    nbytes : int
        The total number of bytes required to store the array data,
        i.e., ``itemsize * size``.
    ndim : int
        The array's number of dimensions.
    shape : tuple of ints
        Shape of the array.
    strides : tuple of ints
        The step-size required to move from one element to the next in
        memory. For example, a contiguous ``(3, 4)`` array of type
        ``int16`` in C-order has strides ``(8, 2)``.  This implies that
        to move from element to element in memory requires jumps of 2 bytes.
        To move from row-to-row, one needs to jump 8 bytes at a time
        (``2 * 4``).
    base : ndarray
        If the array is a view into another array, that array is its `base`
        (unless that array is also a view).  The `base` array is where the
        array data is actually stored.
    __array_interface__ : dict
        Dictionary with low level array information. Used by numpy to
        turn into a real numpy array. Can also be used to give C libraries
        access to the data via ctypes.
    
    See Also
    --------
    array : Construct an array.
    zeros : Create an array, each element of which is zero.
    empty : Create an array, but leave its allocated memory unchanged (i.e.,
            it contains "garbage").
    
    Notes
    -----
    There are two modes of creating an array:

    1. If `buffer` is None, then only `shape`, `dtype`, and `order`
       are used.
    2. If `buffer` is an object exposing the buffer interface, then
       all keywords are interpreted.
    
    """
    
    __slots__ = ['_dtype', '_shape', '_strides', '_itemsize', 
                 '_offset', '_base', '_data']
    
    def __init__(self, shape, dtype='float64', buffer=None, offset=0,
                 strides=None, order=None):
        # Check order
        if order is not None:
            raise RuntimeError('ndarray order parameter is not supported')
        # Check and set shape
        try : 
            assert isinstance(shape, Iterable)
            shape = tuple(shape)
        except Exception as e:
            raise AssertionError('The shape must be tuple or list')
        assert all([isinstance(x, int) for x in shape])
        self._shape = shape
        # Check and set dtype
        dtype = _convert_dtype(dtype) if (dtype is not None) else 'float64'
        if dtype not in _known_dtypes:
            raise TypeError('data type %r not understood' % dtype)
        self._dtype = dtype
        # Itemsize is directly derived from dtype
        self._itemsize = int(_convert_dtype(dtype, 'short')[-1])
        
        if buffer is None:
            # New array
            self._base = None
            # Check and set offset and strides
            assert offset == 0
            self._offset = 0
            assert strides is None
            self._strides = _strides_for_shape(self._shape, self.itemsize)
        
        else:
            # Existing array
            if isinstance(buffer, ndarray) and buffer.base is not None:
                buffer = buffer.base
            # Keep a reference to avoid memory cleanup
            self._base = buffer
            # for ndarray we use the data property
            if isinstance(buffer, ndarray):
                buffer = buffer.data
            # Check and set offset
            assert isinstance(offset, int) and offset >= 0
            self._offset = offset
            # Check and set strides
            if strides is None:
                strides = _strides_for_shape(shape, self.itemsize)
            assert isinstance(strides, tuple)
            assert all([isinstance(x, int) for x in strides])
            assert len(strides) == len(shape)
            self._strides = strides
        
        # Define our buffer class
        buffersize = self._strides[0] * self._shape[0] // self._itemsize
        buffersize += self._offset
        BufferClass = _convert_dtype(dtype, 'ctypes') * buffersize
        # Create buffer
        if buffer is None:
            self._data = BufferClass()
        elif isinstance(buffer, ctypes.Array):
            self._data = BufferClass.from_address(ctypes.addressof(buffer))
        else:
            self._data = BufferClass.from_buffer(buffer)
    
    @property
    def __array_interface__(self):
        """ Allow converting to real numpy array, or pass pointer to C library
        http://docs.scipy.org/doc/numpy/reference/arrays.interface.html
        """
        readonly = False
        # typestr
        typestr = '<' + _convert_dtype(self.dtype, 'short')
        # Pointer
        if isinstance(self._data, ctypes.Array):
            ptr = ctypes.addressof(self._data)
        elif hasattr(self._data, '__array_interface__'):
            ptr, readonly = self._data.__array_interface__['data']
        elif hasattr(self._data, 'buffer_info'):  # Python's array.array
            ptr = self._data.buffer_info()[0]
        elif isinstance(self._data, bytes):
            ptr = ctypes.cast(self._data, ctypes.c_void_p).value
            readonly = True
        else:
            raise TypeError('Cannot get address to underlying array data')
        ptr += self._offset * self.itemsize
        #
        return dict(version=3,
                    shape=self.shape,
                    typestr=typestr,
                    descr=[('', typestr)],
                    data=(ptr, readonly),
                    strides=self.strides,
                    #offset=self._offset,
                    #mask=None,
                    )
    
    def __len__(self):
        return self.shape[0]
    
    def __getitem__(self, key):
        offset, shape, strides = self._index_helper(key)
        if not shape:
            # Return scalar
            return self._data[offset]
        else:
            # Return view
            return ndarray(shape, self.dtype,
                           offset=offset, strides=strides, buffer=self)
    
    def __setitem__(self, key, value):
        
        # Get info for view
        offset, shape, strides = self._index_helper(key)
        
        # Is this easy?
        if not shape:
            self._data[offset] = value
            return

        # Create view to set data to
        view = ndarray(shape, self.dtype,
                        offset=offset, strides=strides, buffer=self)
        
        # Get data to set as a list (because getting slices from ctype
        # arrays yield lists anyway). The list is our "contiguous array" 
        if isinstance(value, (float, int)):
            value_list = [value] * view.size
        elif isinstance(value, (tuple, list)):
            value_list = value
        else:
            if not isinstance(value, ndarray):
                value = array(value, copy=False)
            value_list = value._toflatlist()
        
        # Check if size match
        if view.size != len(value_list):
            raise ValueError('Number of elements in source does not match '
                                'number of elements in target.')
        
        # Assign data in most efficient way that we can. This code
        # looks for the largest semi-contiguous block: the block that
        # we can access as a 1D array with a stepsize.
        subviews = [view]
        value_index = 0
        count = 0
        while subviews:
            subview = subviews.pop(0)
            step = _get_step(subview)
            if step:
                block = value_list[value_index:value_index+subview.size]
                s = slice(subview._offset, 
                            subview._offset + subview.size * step, 
                            step)
                view._data[s] = block
                value_index += subview.size
                count += 1
            else:
                for i in range(subview.shape[0]):
                    subviews.append(subview[i])
        assert value_index == len(value_list)
    
    def __float__(self):
        if self.size == 1:
            return float(self.data[self._offset])
        else:
            raise TypeError('Only length-1 arrays can be converted to scalar')
    
    def __int__(self):
        if self.size == 1:
            return int(self.data[self._offset])
        else:
            raise TypeError('Only length-1 arrays can be converted to scalar')
    
    def __repr__(self):
        # If more than 100 elements, show short repr
        if self.size > 100:
            shapestr = 'x'.join([str(i) for i in self.shape])
            return '<ndarray %s %s at 0x%x>' % (shapestr, self.dtype, id(self))
        # Otherwise, try to show in nice way
        def _repr_r(s, axis, offset):
            axisindent = min(2, max(0, (self.ndim - axis - 1)))
            if axis < len(self.shape):
                s += '['
                for k_index, k in enumerate(xrange(self.shape[axis])):
                    if k_index > 0:
                        s += ('\n       ' + ' ' * axis)  * axisindent
                    offset_ = offset + k * self._strides[axis] // self.itemsize
                    s = _repr_r(s, axis+1, offset_)
                    if k_index < self.shape[axis] - 1:
                        s += ', '
                s += ']'
            else:
                r = repr(self.data[offset])
                if '.' in r:
                    r = ' ' + r
                    if r.endswith('.0'):
                        r = r[:-1]
                s += r
            return s

        s = _repr_r('', 0, self._offset)
        if self.dtype != 'float64' and self.dtype != 'int32':
            return "array(" + s + ", dtype='%s')" % self.dtype
        else:
            return "array(" + s + ")"
    
    def __eq__(self, other):
        if other.__module__.split('.')[0] == 'numpy':
            return other == self
        else:
            out = empty(self.shape, 'bool')
            out[:] = [i1==i2 for (i1, i2) in zip(self.flat, other.flat)]
            return out
    
    def __add__(self, other):
        \'''classic addition
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            out = empty(self.shape, self.dtype)
            out[:] = [dat+other for dat in self._data] 
            return out
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                out = empty(self.shape, self.dtype)
                out[:] = [i+j for (i,j) in zip(self.flat, other.flat)]
                return out

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if (isinstance(other, int) or isinstance(other, float)) :
            out = empty(self.shape, self.dtype)
            out[:] = [dat-other for dat in self._data] 
            return out
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                out = empty(self.shape, self.dtype)
                out[:] = [i-j for (i,j) in zip(self.flat, other.flat)]
                return out

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        \'''multiply element-wise with array or float/scalar\'''
        if (isinstance(other, int) or isinstance(other, float)) :
            out = empty(self.shape, self.dtype)
            out[:] = [dat*other for dat in self._data] 
            return out
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                out = empty(self.shape, self.dtype)
                out[:] = [i*j for (i,j) in zip(self.flat, other.flat)]
                return out       

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        \'''divide element-wise with array or float/scalar\'''
        if (isinstance(other, int) or isinstance(other, float)) :
            if other == 0 : raise ZeroDivisionError
            out = empty(self.shape, self.dtype)
            out[:] = [dat/other for dat in self._data] 
            return out
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                out = empty(self.shape, self.dtype)
                out[:] = [i/j for (i,j) in zip(self.flat, other.flat)]
                return out
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __truediv__(self, other):
        \'''divide element-wise with array or float/scalar\'''
        if (isinstance(other, int) or isinstance(other, float)) :
            if other == 0 : raise ZeroDivisionError
            out = empty(self.shape, self.dtype)
            out[:] = [dat/other for dat in self._data] 
            return out
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                out = empty(self.shape, self.dtype)
                out[:] = [i/j for (i,j) in zip(self.flat, other.flat)]
                return out
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __floordiv__(self, other):
        \'''divide element-wise with array or float/scalar\'''
        if (isinstance(other, int) or isinstance(other, float)) :
            if other == 0 : raise ZeroDivisionError
            out = empty(self.shape, self.dtype)
            out[:] = [dat//other for dat in self._data] 
            return out
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                out = empty(self.shape, self.dtype)
                out[:] = [i//j for (i,j) in zip(self.flat, other.flat)]
                return out
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __mod__(self, other):
        \'''divide element-wise with array or float/scalar\'''
        if (isinstance(other, int) or isinstance(other, float)) :
            out = empty(self.shape, self.dtype)
            out[:] = [dat%other for dat in self._data] 
            return out
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                out = empty(self.shape, self.dtype)
                out[:] = [i%j for (i,j) in zip(self.flat, other.flat)]
                return out
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __pow__(self, other):
        \'''power of two arrays element-wise (of just float power)\'''
        if (isinstance(other, int) or isinstance(other, float)) :
            out = empty(self.shape, self.dtype)
            out[:] = [dat**other for dat in self._data] 
            return out
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                out = empty(self.shape, self.dtype)
                out[:] = [i**j for (i,j) in zip(self.flat, other.flat)]
                return out
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __iadd__(self, other):
        \'''Addition of other array or float in place with += operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            for i in range(len(self._data)):
                self._data[i]+=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]+=other._data[i]
                return self            
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __isub__(self, other):
        \'''Addition of other array or float in place with += operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            for i in range(len(self._data)):
                self._data[i]-=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]-=other._data[i]
                return self
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __imul__(self, other):
        \'''multiplication woth other array or float in place with *= operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            for i in range(len(self._data)):
                self._data[i]*=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]*=other._data[i]
                return self
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __idiv__(self, other):
        \'''Division of other array or float in place with /= operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            if other == 0 : raise ZeroDivisionError
            for i in range(len(self._data)):
                self._data[i]/=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]/=other._data[i]
                return self
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __itruediv__(self, other):
        \'''Division of other array or float in place with /= operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            if other == 0 : raise ZeroDivisionError
            for i in range(len(self._data)):
                self._data[i]/=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]/=other._data[i]
                return self
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __ifloordiv__(self, other):
        \'''Division of other array or float in place with /= operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            if other == 0 : raise ZeroDivisionError
            for i in range(len(self._data)):
                self._data[i]//=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]//=other._data[i]
                return self
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __imod__(self, other):
        \'''mod of other array or float in place with /= operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            if other == 0 : raise ZeroDivisionError
            for i in range(len(self._data)):
                self._data[i]%=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]%=other._data[i]
                return self
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __imod__(self, other):
        \'''mod of other array or float in place with /= operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            if other == 0 : raise ZeroDivisionError
            for i in range(len(self._data)):
                self._data[i]%=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]%=other._data[i]
                return self
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))

    def __ipow__(self, other):
        \'''mod of other array or float in place with /= operator
        \'''
        if (isinstance(other, int) or isinstance(other, float)) :
            for i in range(len(self._data)):
                self._data[i]**=other
            return self
        if (isinstance(other, ndarray)):
            if self.shape == other.shape :
                for i in range(len(self._data)):
                    self._data[i]**=other._data[i]
                return self
            else :
                raise ValueError('Array sizes do not match. '+str(self.shape)\
                                                  +' versus '+str(other.shape))


    ## Private helper functions
    
    def _index_helper(self, key):
        
        # Indexing spec is located at:
        # http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html

        # Promote to tuple.
        if not isinstance(key, tuple):
            key = (key,)

        axis = 0
        shape = []
        strides = []
        offset = self._offset

        for k in key:
            axissize = self._shape[axis]
            if isinstance(k, int):
                if k >= axissize:
                    raise IndexError('index %i is out of bounds for axis %i '
                                     'with size %s' % (k, axis, axissize))
                offset += k * self._strides[axis] // self.itemsize
                axis += 1
            elif isinstance(k, slice):
                start, stop, step = k.indices(self.shape[axis])
                shape.append(_ceildiv(stop - start, step))
                strides.append(step * self._strides[axis])
                offset += start * self._strides[axis] // self.itemsize
                axis += 1
            elif k is Ellipsis:
                raise TypeError("ellipsis are not supported.")
            elif k is None:
                shape.append(1)
                stride = 1
                for s in self._strides[axis:]:
                    stride *= s
                strides.append(stride)
            else:
                raise TypeError("key elements must be instaces of int or slice.")

        shape.extend(self.shape[axis:])
        strides.extend(self._strides[axis:])
        
        return offset, tuple(shape), tuple(strides)
    
    def _toflatlist(self):
        value_list = []
        subviews = [self]
        count = 0
        while subviews:
            subview = subviews.pop(0)
            step = _get_step(subview)
            if step:
                s = slice(subview._offset, 
                          subview._offset + subview.size * step, 
                          step)
                value_list += self._data[s]
                count += 1
            else:
                for i in range(subview.shape[0]):
                    subviews.append(subview[i])
        return value_list
    
    ## Properties
    
    @property
    def ndim(self):
        return len(self._shape)
    
    @property
    def size(self):
        return _size_for_shape(self._shape)
    
    @property
    def nbytes(self):
        return _size_for_shape(self._shape) * self.itemsize
    
    def _get_shape(self):
        return self._shape
    
    def _set_shape(self, newshape):
        if newshape == self.shape:
            return
        if self.size != _size_for_shape(newshape):
            raise ValueError('Total size of new array must be unchanged')
        if _get_step(self) == 1:
            # Contiguous, hooray!
            self._shape = tuple(newshape)
            self._strides = _strides_for_shape(self._shape, self.itemsize)
            return
        
        # Else, try harder ... This code supports adding /removing
        # singleton dimensions. Although it may sometimes be possible
        # to split a dimension in two if the contiguous blocks allow
        # this, we don't bother with such complex cases for now.
        # Squeeze shape / strides 
        N = self.ndim
        shape = [self.shape[i] for i in range(N) if self.shape[i] > 1]
        strides = [self.strides[i] for i in range(N) if self.shape[i] > 1]
        # Check if squeezed shapes match
        newshape_ = [newshape[i] for i in range(len(newshape)) 
                     if newshape[i] > 1]
        if newshape_ != shape:
            raise AttributeError('incompatible shape for non-contiguous array')
        # Modify to make this data work in loop
        strides.append(strides[-1])
        shape.append(1)
        # Form new strides
        i = -1
        newstrides = []
        try:
            for s in reversed(newshape):
                if s == 1:
                    newstrides.append(strides[i] * shape[i])
                else:
                    i -= 1
                    newstrides.append(strides[i])
        except IndexError:
            # Fail
            raise AttributeError('incompatible shape for non-contiguous array')
        else:
            # Success
            newstrides.reverse()
            self._shape = tuple(newshape)
            self._strides = tuple(newstrides)
    
    shape = property(_get_shape, _set_shape)  # Python 2.5 compat (e.g. Jython)
    
    @property
    def strides(self):
        return self._strides
    
    @property
    def dtype(self):
        return self._dtype
    
    @property
    def itemsize(self):
        return self._itemsize
    
    @property
    def base(self):
        return self._base
    
    @property
    def data(self):
        return self._data
    
    @property
    def flat(self):
        subviews = [self]
        count = 0
        while subviews:
            subview = subviews.pop(0)
            step = _get_step(subview)
            if step:
                s = slice(subview._offset, 
                          subview._offset + subview.size * step, 
                          step)
                for i in self._data[s]:
                    yield i
            else:
                for i in range(subview.shape[0]):
                    subviews.append(subview[i])
    
    @property
    def T(self):
        if self.ndim < 2:
            return self
        else:
            return self.transpose()
    
    @property
    def flags(self):
        
        c_cont = _get_step(self) == 1
        return dict(C_CONTIGUOUS=c_cont,
                    F_CONTIGUOUS=(c_cont and self.ndim < 2),
                    OWNDATA=(self._base is None),
                    WRITEABLE=True, # todo: fix this
                    ALIGNED=c_cont,  # todo: different from contiguous?
                    UPDATEIFCOPY=False,  # We don't support this feature
               )
    
    ## Methods - managemenet
    
    def fill(self, value):
        assert isinstance(value, (int, float))
        self[:] = value
    
    def clip(self, a_min, a_max, out=None):
        if out is None:
            out = empty(self.shape, self.dtype)
        L = self._toflatlist()
        L = [min(a_max, max(a_min, x)) for x in L]
        out[:] = L
        return out
    
    def copy(self):
        out = empty(self.shape, self.dtype)
        out[:] = self
        return out
    
    def flatten(self):
        out = empty((self.size,), self.dtype)
        out[:] = self
        return out
    
    def ravel(self):
        return self.reshape((self.size, ))
    
    def repeat(self, repeats, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        out = empty((self.size * repeats,), self.dtype)
        for i in range(repeats):
            out[i*self.size:(i+1)*self.size] = self
        return out
    
    def reshape(self, newshape):
        out = self.view()
        try:
            out.shape = newshape
        except AttributeError:
            out = self.copy()
            out.shape = newshape
        return out
    
    def transpose(self):
        # Numpy returns a view, but we cannot do that since we do not
        # support Fortran ordering
        ndim = self.ndim
        if ndim < 2:
            return self.view()
        shape = self.shape[::-1]
        out = empty(shape, self.dtype)
        #
        if ndim == 2:
            for i in xrange(self.shape[0]):
                out[:, i] = self[i, :]
        elif ndim == 3:
            for i in xrange(self.shape[0]):
                for j in xrange(self.shape[1]):
                    out[:, j, i] = self[i, j, :]
        else:
            raise ValueError('Tinynumpy supports transpose up to ndim=3')
        return out
    
    def astype(self, dtype):
        out = empty(self.shape, dtype)
        out[:] = self
    
    def view(self, dtype=None, type=None):
        if dtype is None:
            dtype = self.dtype
        if dtype == self.dtype:
            return ndarray(self.shape, dtype, buffer=self, 
                           offset=self._offset, strides=self.strides)
        elif self.ndim == 1:
            itemsize = int(_convert_dtype(dtype, 'short')[-1])
            size = self.nbytes // itemsize
            offsetinbytes = self._offset * self.itemsize
            offset = offsetinbytes // itemsize
            return ndarray((size, ), dtype, buffer=self, offset=offset)
        else:
            raise ValueError('new type not compatible with array.')
    
    ## Methods - statistics
    
    # We use the self.flat generator here. self._toflatlist() would be
    # faster, but it might take up significantly more memory.
    
    def all(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        return all(self.flat)
    
    def any(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        return any(self.flat)
    
    def min(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        return min(self.flat)
    
    def max(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        return max(self.flat)
        #return max(self._toflatlist())  # almost twice as fast
    
    def sum(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        return sum(self.flat)
    
    def prod(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        p = 1.0
        for i in self.flat:
            p *= float(i)
        return p
        
    def ptp(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        mn = self.data[self._offset]
        mx = mn
        for i in self.flat:
            if i > mx:
                mx = i
            if i < mn:
                mn = i
        return mx - mn

    def mean(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        return self.sum() / self.size
    
    def argmax(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        r = self.data[self._offset]
        r_index = 0
        for i_index, i in enumerate(self.flat):
            if i > r:
                r = i
                r_index = i_index
        return r_index

    def argmin(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        r = self.data[self._offset]
        r_index = 0
        for i_index, i in enumerate(self.flat):
            if i < r:
                r = i
                r_index = i_index
        return r_index
    
    def cumprod(self, axis=None, out=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        if out is None:
            out = empty((self.size,), self.dtype)
        p = 1
        L = []
        for x in self.flat:
            p *= x
            L.append(p)
        out[:] = L
        return out

    def cumsum(self, axis=None, out=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        if out is None:
            out = empty((self.size,), self.dtype)
        p = 0
        L = []
        for x in self.flat:
            p += x
            L.append(p)
        out[:] = L
        return out

    def var(self, axis=None):
        if axis:
            raise (TypeError, "axis argument is not supported")
        m = self.mean()
        acc = 0
        for x in self.flat:
            acc += abs(x - m) ** 2
        return acc / self.size

    def std(self, axis=None):
        return sqrt(self.var(axis))

    def argwhere(self, val):
        #assumes that list has only values of same dtype

        idx  = [i for i, e in enumerate(self.flat) if e == val]
        keys = [list(_key_for_index(i, self.shape)) for i in idx]
        return keys

    def tolist(self):
        \'''
        Returns the ndarray as a comprehensive list 
        \'''
        shp    = list(self.shape).copy()
        jump   = self.size//shp[-1]
        n_comp = 0 #comprehension depth
        comp   = list(self._data).copy()
        while n_comp < len(self.shape)-1 :
            comp = [comp[i*shp[-1]:i*shp[-1]+shp[-1]] for i in range(jump)]
            shp.pop()
            jump = len(comp)//shp[-1]
            n_comp +=1
        return comp




class nditer:
    def __init__(self, array):
        self.array = array
        self.key = [0] * len(self.array.shape)

    def __iter__(self):
        return self

    def __len__(self):
        return _size_for_shape(self.array.shape)

    def __getitem__(self, index):
        key = _key_for_index(index, self.array.shape)
        return self.array[key]

    def __next__(self):
        if self.key is None:
            raise StopIteration
        value = self.array[tuple(self.key)]
        if not _increment_mutable_key(self.key, self.array.shape):
            self.key = None
        return value

    def next(self):
        return self.__next__()'''


inliner_packages = {
    "numpy": [
        1, 2782, 2782, 1716497050.825598],
    "numpy.test_tinyndarray": [
        0, 2782, 8138, 1716497050.825598],
    "numpy.test_tinynumpy": [
        0, 8138, 19829, 1716497050.825598],
    "numpy.benchmark": [
        0, 19829, 23506, 1716497050.825598],
    "numpy.tinylinalg": [
        0, 23506, 24367, 1716497050.825598],
    "numpy.tinynumpy": [
        0, 24367, 74642, 1716497244.605566]
}


def prepare_package():
    # Loader's module name changes with each major version to be able to have
    # different loaders working at the same time.
    module_name = PINLINER_MODULE_NAME + '_' + loader_version.split('.')[0]

    # If the loader code is not already loaded we create a specific module for
    # it.  We need to do it this way so that the functions in there are not
    # compiled with a reference to this module's global dictionary in
    # __globals__.
    module = sys.modules.get(module_name)
    if not module:
        module = types.ModuleType(module_name)
        module.__package__ = ''
        module.__file__ = module_name + '.py'
        exec(inliner_importer_code, module.__dict__)
        sys.modules[module_name] = module

    # We cannot use __file__ directly because on the second run __file__ will
    # be the compiled file (.pyc) and that's not the file we want to read.
    filename = os.path.splitext(__file__)[0] + '.py'

    # Add our own finder and loader for this specific package if it's not
    # already there.
    # This must be done before we initialize the package, as it may import
    # packages and modules contained in the package itself.
    for finder in sys.meta_path:
        if (isinstance(finder, module.InlinerImporter) and
                finder.data == inliner_packages):
            importer = finder
    else:
        # If we haven't forced the setting of the uncaught exception handler
        # we replace it only if it hasn't been replace yet, this is because
        # CPython default handler does not use traceback or even linecache, so
        # it never calls get_source method to get the code, but for example
        # iPython does, so we don't need to replace the handler.
        if FORCE_EXC_HOOK is None:
            set_excepthook = sys.__excepthook__ == sys.excepthook
        else:
            set_excepthook = FORCE_EXC_HOOK

        importer = module.InlinerImporter(inliner_packages, filename,
                                          set_excepthook)
        sys.meta_path.append(importer)

    # If this is a bundle (multiple packages) without default then don't import
    # any package automatically.
    if not PINLINED_DEFAULT_PACKAGE:
        return

    __, start, end, ts = inliner_packages[PINLINED_DEFAULT_PACKAGE]
    with open(filename) as datafile:
        datafile.seek(start)
        code = datafile.read(end - start)

    # We need everything to be local variables before we clear the global dict
    def_package = PINLINED_DEFAULT_PACKAGE
    name = __name__
    filename = def_package + '/__init__.py'
    compiled_code = compile(code, filename, 'exec')

    # Prepare globals to execute __init__ code
    globals().clear()
    # If we've been called directly we cannot set __path__
    if name != '__main__':
        globals()['__path__'] = [def_package]
    else:
        def_package = None
    globals().update(__file__=filename,
                     __package__=def_package,
                     __name__=name,
                     __loader__=importer)

    exec(compiled_code, globals())


# Prepare loader's module and populate this namespace only with package's
# __init__
prepare_package()