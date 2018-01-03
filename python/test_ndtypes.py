#
# BSD 3-Clause License
#
# Copyright (c) 2017, plures
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import sys, argparse
import unittest, gc
import weakref, struct
from copy import copy
from ndtypes import ndt, typedef, MAX_DIM
from randtype import *


HAVE_PYTHON_36 = sys.version_info >= (3, 6, 0)


class TestModule(unittest.TestCase):

    def test_module_predicates(self):
        # Namespaces are not yet supported in xnd. One can construct the
        # types, however.  Modules are for pattern matching only, so they 
        # are abstract.
        t = ndt("SomeNamespace:: 2 * 3 * float64")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_f_contiguous())
        self.assertFalse(t.is_c_contiguous())

    def test_module_common_fields(self):
        t = ndt("SomeNamespace:: 2 * 3 * float64")

        # Common type fields are undefined.
        self.assertRaises(TypeError, getattr, t, 'ndim')
        self.assertRaises(TypeError, getattr, t, 'itemsize')
        self.assertRaises(TypeError, getattr, t, 'align')

        # Cannot be represented as an ndarray.
        self.assertRaises(TypeError, getattr, t, 'shape')
        self.assertRaises(TypeError, getattr, t, 'strides')


class TestFunction(unittest.TestCase):

    def test_function_predicates(self):
        t = ndt("(10 * float64, string) -> float64")
 
        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_function_common_fields(self):
        t = ndt("(10 * float64, string) -> float64")

        # Common type fields are undefined.
        self.assertRaises(TypeError, getattr, t, 'ndim')
        self.assertRaises(TypeError, getattr, t, 'itemsize')
        self.assertRaises(TypeError, getattr, t, 'align')

        # Cannot be represented as an ndarray.
        self.assertRaises(TypeError, getattr, t, 'shape')
        self.assertRaises(TypeError, getattr, t, 'strides')


class TestVoid(unittest.TestCase):

    def test_void_as_return_value(self):
        t = ndt("() -> void")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_void_exceptions(self):
        # Void can only be used as a function return type.
        self.assertRaises(ValueError, ndt, "void")


class TestAny(unittest.TestCase):

    def test_any_predicates(self):
        t = ndt("Any")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_any_common_fields(self):
        t = ndt("Any")

        # Common type fields are undefined.
        self.assertRaises(TypeError, getattr, t, 'ndim')
        self.assertRaises(TypeError, getattr, t, 'itemsize')
        self.assertRaises(TypeError, getattr, t, 'align')

        # Cannot be represented as an ndarray.
        self.assertRaises(TypeError, getattr, t, 'shape')
        self.assertRaises(TypeError, getattr, t, 'strides')


class TestFixedDim(unittest.TestCase):

    def test_fixed_dim_predicates(self):
        t = ndt("10 * 20 * complex128")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertTrue(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

        t = ndt("20 * complex128")
        self.assertTrue(t.is_c_contiguous())
        self.assertTrue(t.is_f_contiguous())

        t = ndt("1 * 10 * complex128")
        self.assertTrue(t.is_c_contiguous())
        self.assertTrue(t.is_f_contiguous())

    def test_fixed_dim_common_fields(self):
        dt = "{a: complex64, b: string}"
        t = ndt("2 * 3 * %s" % dt)
        dtype = ndt(dt)

        self.assertEqual(t.ndim, 2)
        self.assertEqual(t.itemsize, dtype.itemsize)
        self.assertEqual(t.align, dtype.align)

        self.assertEqual(t.shape, (2, 3))
        self.assertEqual(t.strides, (3 * dtype.itemsize, dtype.itemsize))

    def test_fixed_dim_invariants(self):
        # Mixing var and fixed is disallowed.
        self.assertRaises(TypeError, ndt, "10 * var * int8")
        self.assertRaises(TypeError, ndt, "var * 10 * int16")
        self.assertRaises(TypeError, ndt, "10 * var * 10 * int32")
        self.assertRaises(TypeError, ndt, "var * 10 * var * int64")

    def test_fixed_dim_dtypes(self):
        for dtype, mem in DTYPE_TEST_CASES:
            t = ndt(dtype)
            self.assertEqual(t.ndim, 0)
            self.assertEqual(t.itemsize, mem.itemsize)
            self.assertEqual(t.align, mem.align)

            self.assertEqual(t.shape, ())
            self.assertEqual(t.strides, ())

            for i in range(10):
                t = ndt("%d * %s" % (i, dtype))
                shape = (i,)
                strides = (mem.itemsize,)

                self.assertEqual(t.ndim, 1)
                self.assertEqual(t.itemsize, mem.itemsize)
                self.assertEqual(t.align, mem.align)

                self.assertEqual(t.shape, shape)
                self.assertEqual(t.strides, strides)

            for i in range(10):
                for j in range(10):
                    t = ndt("%d * %d * %s" % (i, j, dtype))
                    shape = (i, j)
                    strides = (j * mem.itemsize, mem.itemsize)

                    self.assertEqual(t.ndim, 2)
                    self.assertEqual(t.itemsize, mem.itemsize)
                    self.assertEqual(t.align, mem.align)

                    self.assertEqual(t.shape, shape)
                    self.assertEqual(t.strides, strides)

            for i in range(5):
                for j in range(5):
                    for k in range(5):
                        t = ndt("%d * %d * %d * %s" % (i, j, k, dtype))
                        shape = (i, j, k)
                        strides = (j * k * mem.itemsize, k * mem.itemsize, mem.itemsize)

                        self.assertEqual(t.ndim, 3)
                        self.assertEqual(t.itemsize, mem.itemsize)
                        self.assertEqual(t.align, mem.align)

                        self.assertEqual(t.shape, shape)
                        self.assertEqual(t.strides, strides)


class TestFortran(unittest.TestCase):

    def test_fortran_predicates(self):
        t = ndt("!10 * 20 * complex128")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertTrue(t.is_f_contiguous())

        t = ndt("!20 * complex128")
        self.assertTrue(t.is_c_contiguous())
        self.assertTrue(t.is_f_contiguous())

        t = ndt("!1 * 10 * uint8")
        self.assertTrue(t.is_c_contiguous())
        self.assertTrue(t.is_f_contiguous())

    def test_fortran_common_fields(self):
        dt = "{a: complex64, b: string}"
        t = ndt("!2 * 3 * %s" % dt)
        dtype = ndt(dt)

        self.assertEqual(t.ndim, 2)
        self.assertEqual(t.itemsize, dtype.itemsize)
        self.assertEqual(t.align, dtype.align)

        self.assertEqual(t.shape, (2, 3))
        self.assertEqual(t.strides, (dtype.itemsize, 2 * dtype.itemsize))

    def test_fortran_dtypes(self):
        for dtype, mem in DTYPE_TEST_CASES:
            t = ndt(dtype)
            self.assertEqual(t.ndim, 0)
            self.assertEqual(t.itemsize, mem.itemsize)
            self.assertEqual(t.align, mem.align)

            self.assertEqual(t.shape, ())
            self.assertEqual(t.strides, ())

            for i in range(10):
                t = ndt("!%d * %s" % (i, dtype))
                shape = (i,)
                strides = (mem.itemsize,)

                self.assertEqual(t.ndim, 1)
                self.assertEqual(t.itemsize, mem.itemsize)
                self.assertEqual(t.align, mem.align)

                self.assertEqual(t.shape, shape)
                self.assertEqual(t.strides, strides)

            for i in range(10):
                for j in range(10):
                    t = ndt("!%d * %d * %s" % (i, j, dtype))
                    shape = (i, j)
                    strides = (mem.itemsize, i * mem.itemsize)

                    self.assertEqual(t.ndim, 2)
                    self.assertEqual(t.itemsize, mem.itemsize)
                    self.assertEqual(t.align, mem.align)

                    self.assertEqual(t.shape, shape)
                    self.assertEqual(t.strides, strides)

            for i in range(5):
                for j in range(5):
                    for k in range(5):
                        t = ndt("!%d * %d * %d * %s" % (i, j, k, dtype))
                        shape = (i, j, k)
                        strides = (mem.itemsize, i * mem.itemsize, i * j * mem.itemsize)

                        self.assertEqual(t.ndim, 3)
                        self.assertEqual(t.itemsize, mem.itemsize)
                        self.assertEqual(t.align, mem.align)

                        self.assertEqual(t.shape, shape)
                        self.assertEqual(t.strides, strides)


class TestVarDim(unittest.TestCase):

    def test_var_dim_predicates(self):
        t = ndt("var(offsets=[0,2]) * var(offsets=[0,3,10]) * complex128")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_var_dim_common_fields(self):
        dt = "{a: complex64, b: string}"
        t = ndt("var(offsets=[0,2]) * var(offsets=[0,3,10]) * %s" % dt)
        dtype = ndt(dt)

        self.assertEqual(t.ndim, 2)
        self.assertEqual(t.itemsize, dtype.itemsize)
        self.assertEqual(t.align, dtype.align)

        self.assertRaises(TypeError, getattr, t, 'shape')
        self.assertRaises(TypeError, getattr, t, 'strides')

    def test_var_dim_invariants(self):
        # Mixing var and fixed is disallowed.
        self.assertRaises(TypeError, ndt, "10 * var * int64")
        self.assertRaises(TypeError, ndt, "var * 10 * int64")
        self.assertRaises(TypeError, ndt, "10 * var * 10 * int64")
        self.assertRaises(TypeError, ndt, "var * 10 * var * int64")
        self.assertRaises(TypeError, ndt, "N * var * int64")
        self.assertRaises(TypeError, ndt, "var * N * int64")
        self.assertRaises(TypeError, ndt, "N * var * N * int64")
        self.assertRaises(TypeError, ndt, "var * N * var * int64")

        # Too many dimensions.
        self.assertRaises(TypeError, ndt, "var * " * (MAX_DIM + 1) + "float64")

        # Nested var is disallowed.
        self.assertRaises(TypeError, ndt, "2 * {a: var * complex128}")
        self.assertRaises(TypeError, ndt, "var * {a: var * complex128}")
        self.assertRaises(TypeError, ndt, "var * ref(var * string)")
        self.assertRaises(TypeError, ndt, "var * SomeConstr(var * string)")

    def test_var_dim_external_offsets(self):
        # Invalid offsets.
        self.assertRaises(TypeError, ndt, "int8", [""])
        self.assertRaises(TypeError, ndt, "int8", [0])
        self.assertRaises(TypeError, ndt, "int8", [0, 2])
        self.assertRaises(TypeError, ndt, "int8", {})
        self.assertRaises(TypeError, ndt, "int8", ())
        self.assertRaises(TypeError, ndt, "int8", [(), ()])

        self.assertRaises(ValueError, ndt, "int8", [])
        self.assertRaises(ValueError, ndt, "int8", [[0]])
        self.assertRaises(ValueError, ndt, "int8", [[0], [0]])

        self.assertRaises(ValueError, ndt, "int8", [[-1, 2]])
        self.assertRaises(ValueError, ndt, "int8", [[0, 2147483648]])

        # Invalid combinations.
        self.assertRaises(ValueError, ndt, "int8", [[0, 2], [0, 10]])
        self.assertRaises(ValueError, ndt, "int8", [[0, 2], [0, 10, 30, 40]])

        # Implicit mixing of var and fixed.
        self.assertRaises(TypeError, ndt, "10 * int8", [[0, 2], [0, 10, 20]])

        # Abstract dtype.
        self.assertRaises(ValueError, ndt, "N * int8", [[0, 2], [0, 10, 20]])
        self.assertRaises(ValueError, ndt, "var * int8", [[0, 2], [0, 10, 20]])

        # Mixing external and internal offsets.
        self.assertRaises(TypeError, ndt, "var(offsets=[0,2,10]) * int8", [[0, 1], [0, 2]])


class TestSymbolicDim(unittest.TestCase):

    def test_symbolic_dim_predicates(self):
        t = ndt("N * M * complex128")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_symbolic_dim_common_fields(self):
        dt = "{a: complex64, b: string}"
        t = ndt("N * M * %s" % dt)
        dtype = ndt(dt)

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestEllipsisDim(unittest.TestCase):

    def test_ellipsis_dim_predicates(self):
        t = ndt("2 * ... * complex128")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_ellipsis_dim_common_fields(self):
        dt = "{a: complex64, b: string}"
        t = ndt("... * 2 * %s" % dt)
        dtype = ndt(dt)

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestTuple(unittest.TestCase):

    def test_tuple_predicates(self):
        for s in ["()", "(int64)", "(string, bytes, pack=1)"]:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

        for s in ["(Any)", "(int64, N * M * uint8)", "(string, Float)"]:
            t = ndt(s)

            self.assertTrue(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertFalse(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_tuple_common_fields(self):
        f = "{a: complex64, b: string}"
        t = ndt("(%s, %s)" % (f, f))
        field = ndt(f)

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, 2 * field.itemsize)
        self.assertEqual(t.align, field.align)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestRecord(unittest.TestCase):

    def test_record_predicates(self):
        for s in ["{}", "{a: int64, b: bytes}", "{x: string, y: uint8, pack=1}"]:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

        for s in ["{a: Any, b: Complex}", "{x: N * M * T}"]:
            t = ndt(s)

            self.assertTrue(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertFalse(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_record_common_fields(self):
        f = "{a: complex64, b: string}"
        t = ndt("{x: %s, y: %s, z: %s}" % (f, f, f))
        field = ndt(f)

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, 3 * field.itemsize)
        self.assertEqual(t.align, field.align)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestRef(unittest.TestCase):

    def test_ref_predicates(self):
        for s in ["&2 * 3 * float64", "&bool", "&(uint8, int32)"]:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

        for s in ["&Any", "&(int64, N * M * uint8)"]:
            t = ndt(s)

            self.assertTrue(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertFalse(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_ref_common_fields(self):
        a = "{a: complex64, b: string}"
        t = ndt("ref(%s)" % a)
        arg = ndt(a)

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, SIZEOF_PTR)
        self.assertEqual(t.align, SIZEOF_PTR)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestConstr(unittest.TestCase):

    def test_constr_predicates(self):
        for s in ["Some(int16)", "Maybe(int64)", "Just((string, bytes))"]:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_constr_common_fields(self):
        a = "{a: complex64, b: string}"
        t = ndt("Just(%s)" % a)
        arg = ndt(a)

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, arg.itemsize)
        self.assertEqual(t.align, arg.align)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestNominal(unittest.TestCase):

    # The regrtest.py -R option causes setUpClass() to be called several times.
    initialized = False

    @classmethod
    def setUpClass(cls):
        if not cls.initialized:
            typedef("some_t", "2 * 10 * complex128")
            cls.initialized = True

    def test_nominal_predicates(self):
            t = ndt("some_t")

            # The nominal type is opaque. The only thing known is that
            # the typedef is concrete.
            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_nominal_common_fields(self):
        t = ndt("some_t")
        dtype = ndt("complex128")

        # The opaque type is treated as a dtype with ndim==0, same as
        # for constructor types.
        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, 2 * 10 * dtype.itemsize)
        self.assertEqual(t.align, dtype.align)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')

    def test_nominal_exceptions(self):
        # not in the typedef table
        self.assertRaises(ValueError, ndt, "undefined_t")

        # duplicate typedef
        self.assertRaises(ValueError, typedef, "some_t", "int64")


class TestScalarKind(unittest.TestCase):

    def test_scalar_kind_predicates(self):
        t = ndt("Scalar")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_scalar_kind_common_fields(self):
        t = ndt("Scalar")

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestCategorical(unittest.TestCase):

    def test_categorical_predicates(self):
        for s in [ 
            "categorical(NA, 1, 100, -29999)",
            "categorical(NA, 1.2, -200.25)",
            "categorical('foo', 'bar')",
            "categorical('foo', NA, 100)"]:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertFalse(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_categorical_common_fields(self):
        t = ndt("categorical(NA, 'something', 'must', 'be', 'done')")

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, 8)
        self.assertEqual(t.align, 8)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestFixedStringKind(unittest.TestCase):

    def test_fixed_string_kind_predicates(self):
        t = ndt("FixedString")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_fixed_string_kind_common_fields(self):
        t = ndt("FixedString")

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestFixedString(unittest.TestCase):

    def test_fixed_string_predicates(self):
        t = ndt("fixed_string(380, 'utf16')")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertTrue(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_fixed_string_common_fields(self):
        for encoding, codepoint_size in [
            ('ascii', 1),
            ('utf8', 1),
            ('utf16', 2),
            ('utf32', 4)]:

            t = ndt("fixed_string(20, '%s')" % encoding)

            self.assertEqual(t.ndim, 0)
            self.assertEqual(t.itemsize, 20 * codepoint_size)
            self.assertEqual(t.align, codepoint_size)

            self.assertRaises(TypeError, t, 'shape')
            self.assertRaises(TypeError, t, 'strides')


class TestFixedBytesKind(unittest.TestCase):

    def test_fixed_bytes_kind_predicates(self):
        t = ndt("FixedBytes")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_fixed_string_kind_common_fields(self):
        t = ndt("FixedBytes")

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestFixedBytes(unittest.TestCase):

    def test_fixed_bytes_predicates(self):
        t = ndt("fixed_bytes(size=1020)")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertTrue(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_fixed_bytes_common_fields(self):
        for align in [1,2,4,8,16,32,64]:

            t = ndt("fixed_bytes(size=1024, align=%d)" % align)

            self.assertEqual(t.ndim, 0)
            self.assertEqual(t.itemsize, 1024)
            self.assertEqual(t.align, align)

            self.assertRaises(TypeError, t, 'shape')
            self.assertRaises(TypeError, t, 'strides')

    def test_fixed_bytes_exceptions(self):
        # Data size must be a multiple of align.
        self.assertRaises(ValueError, ndt, "fixed_bytes(size=20, align=8)")


class TestString(unittest.TestCase):

    def test_string_predicates(self):
        t = ndt("string")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertTrue(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_string_common_fields(self):
        t = ndt("string")

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, SIZEOF_PTR)
        self.assertEqual(t.align, SIZEOF_PTR)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestBytes(unittest.TestCase):

    def test_bytes_predicates(self):
        t = ndt("bytes")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertTrue(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_bytes_common_fields(self):
        t = ndt("bytes")

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, 16)
        self.assertEqual(t.align, 8)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestChar(unittest.TestCase):

    def test_char_predicates(self):
        t = ndt("char")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertTrue(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_char_common_fields(self):
        t = ndt("char('utf32')")

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, 4)
        self.assertEqual(t.align, 4)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestBool(unittest.TestCase):

    def test_bool_predicates(self):
        t = ndt("bool")

        self.assertFalse(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertTrue(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertTrue(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_bool_common_fields(self):
        t = ndt("bool")

        self.assertEqual(t.ndim, 0)
        self.assertEqual(t.itemsize, 1)
        self.assertEqual(t.align, 1)

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestSignedKind(unittest.TestCase):

    def test_signed_kind_predicates(self):
        t = ndt("Signed")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_signed_kind_common_fields(self):
        t = ndt("Signed")

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestSigned(unittest.TestCase):

    def test_signed_predicates(self):
        signed = ['int8', 'int16', 'int32', 'int64']

        for s in signed:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertTrue(t.isscalar())
            self.assertTrue(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_signed_common_fields(self):
        for s, itemsize in [
            ('int8', 1),
            ('int16', 2),
            ('int32', 4),
            ('int64', 8)]:

            t = ndt(s)

            self.assertEqual(t.ndim, 0)
            self.assertEqual(t.itemsize, itemsize)
            self.assertEqual(t.align, itemsize)

            self.assertRaises(TypeError, t, 'shape')
            self.assertRaises(TypeError, t, 'shape')


class TestUnsignedKind(unittest.TestCase):

    def test_unsigned_kind_predicates(self):
        t = ndt("Unsigned")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_unsigned_kind_common_fields(self):
        t = ndt("Unsigned")

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestUnsigned(unittest.TestCase):

    def test_unsigned_predicates(self):
        unsigned = ['uint8', 'uint16', 'uint32', 'uint64']

        for s in unsigned:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertTrue(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertTrue(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_unsigned_common_fields(self):
        for s, itemsize in [
            ('uint8', 1),
            ('uint16', 2),
            ('uint32', 4),
            ('uint64', 8)]:

            t = ndt(s)

            self.assertEqual(t.ndim, 0)
            self.assertEqual(t.itemsize, itemsize)
            self.assertEqual(t.align, itemsize)

            self.assertRaises(TypeError, t, 'shape')
            self.assertRaises(TypeError, t, 'shape')


class TestFloatKind(unittest.TestCase):

    def test_float_kind_predicates(self):
        t = ndt("Float")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_float_kind_common_fields(self):
        t = ndt("Float")

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestFloat(unittest.TestCase):

    def test_float_predicates(self):
        _float = ['float32', 'float64']
        if HAVE_PYTHON_36:
            _float.insert(0, 'float16')

        for s in _float:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertFalse(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertTrue(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertTrue(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_float_common_fields(self):
        _float = [('float32', 4), ('float64', 8)]
        if HAVE_PYTHON_36:
            _float.insert(0, ('float16', 2))

        for s, itemsize in _float:
            t = ndt(s)

            self.assertEqual(t.ndim, 0)
            self.assertEqual(t.itemsize, itemsize)
            self.assertEqual(t.align, itemsize)

            self.assertRaises(TypeError, t, 'shape')
            self.assertRaises(TypeError, t, 'shape')


class TestComplexKind(unittest.TestCase):

    def test_complex_kind_predicates(self):
        t = ndt("Complex")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_complex_kind_common_fields(self):
        t = ndt("Complex")

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestComplex(unittest.TestCase):

    def test_complex_predicates(self):
        _complex = ['complex64', 'complex128']
        if HAVE_PYTHON_36:
            _complex.insert(0, 'complex32')

        for s in _complex:
            t = ndt(s)

            self.assertFalse(t.isabstract())
            self.assertTrue(t.iscomplex())
            self.assertTrue(t.isconcrete())
            self.assertFalse(t.isfloat())
            self.assertFalse(t.isoptional())
            self.assertTrue(t.isscalar())
            self.assertFalse(t.issigned())
            self.assertFalse(t.isunsigned())

            self.assertFalse(t.is_c_contiguous())
            self.assertFalse(t.is_f_contiguous())

    def test_complex_common_fields(self):
        _complex = [('complex64', 8), ('complex128', 16)]
        if HAVE_PYTHON_36:
            _complex.insert(0, ('complex32', 4))

        for s, itemsize in _complex:
            t = ndt(s)

            self.assertEqual(t.ndim, 0)
            self.assertEqual(t.itemsize, itemsize)
            self.assertEqual(t.align, itemsize / 2)

            self.assertRaises(TypeError, t, 'shape')
            self.assertRaises(TypeError, t, 'shape')


class TestTypevar(unittest.TestCase):

    def test_typevar_predicates(self):
        t = ndt("T")

        self.assertTrue(t.isabstract())
        self.assertFalse(t.iscomplex())
        self.assertFalse(t.isconcrete())
        self.assertFalse(t.isfloat())
        self.assertFalse(t.isoptional())
        self.assertFalse(t.isscalar())
        self.assertFalse(t.issigned())
        self.assertFalse(t.isunsigned())

        self.assertFalse(t.is_c_contiguous())
        self.assertFalse(t.is_f_contiguous())

    def test_typevar_common_fields(self):
        t = ndt("T")

        self.assertRaises(TypeError, t, 'ndim')
        self.assertRaises(TypeError, t, 'itemsize')
        self.assertRaises(TypeError, t, 'align')

        self.assertRaises(TypeError, t, 'shape')
        self.assertRaises(TypeError, t, 'strides')


class TestCopy(unittest.TestCase):

    def test_copy(self):
        for dtype, mem in DTYPE_TEST_CASES:
            t = ndt(dtype)
            u = copy(t)
            self.assertEqual(u, t)
            self.assertEqual(u.ast_repr(), t.ast_repr())

    def test_copy_gc(self):
        class MyType(ndt):
            self.attr = None
        class MyObject():
            self.attr = None

        x = ndt("var(offsets=[0,2]) * var(offsets=[0,3,10]) * int8")
        y = copy(x)
        x = y = None
        gc.collect()

        x = ndt("{z: 10 * int8}", [[0, 2], [0, 10, 20]])
        y = copy(x)
        x = y = None
        gc.collect()

        x = MyType("var(offsets=[0,2]) * var(offsets=[0,3,10]) * int8")
        y = copy(x)
        o = MyObject()
        o.attr = x
        x.attr = y
        y.attr = o
        wr = weakref.ref(o)
        x = y = o = None
        gc.collect()
        self.assertTrue(wr() is None, wr())


class TestBufferProtocol(unittest.TestCase):

    def test_array(self):
        test_cases = [
            # format, itemsize, alignment
            ("(0)f", 4, 4),
            ("(1)d", 8, 8),
            ("(125)d", 8, 8),
            ("(2,3)d", 8, 8),
            ("(2,10)T{<b:a:Q:b:}", 9, 1),
            ("(2,19)T{<b:a:xxxQ:b:}", 12, 4),
            ("(31,221)T{<b:a:xxxxxxxQ:b:}", 16, 8),
            ("(2,3,10)T{<b:a:xxxxxxxxxxxxxxxQ:b:xxxxxxxx}", 32, 16),
            ("(2,10)T{=L:a:(2,3)Zd:b:}", 100, 1)]

        test_error_cases = [
            # empty shape (scalars are not arrays in datashape)
            "()Q",
            # Ambiguous (tuple of 10 or array of 10)?
            "10Q"]

        for fmt, itemsize, align in test_cases:
            t = ndt.from_format(fmt)
            self.assertEqual(t.itemsize, itemsize)
            self.assertEqual(t.align, align)

        for fmt in test_error_cases:
            self.assertRaises(ValueError, ndt.from_format, fmt)

    def test_record(self):
        test_cases = [
            # format, itemsize, alignment
            ("T{<b:a:Q:b:}", 9, 1),
            ("T{<b:a:xQ:b:}", 10, 2),
            ("T{<b:a:xxxQ:b:}", 12, 4),
            ("T{<b:a:xxxxxxxQ:b:}", 16, 8),
            ("T{<b:a:xxxxxxxxxxxxxxxQ:b:xxxxxxxx}", 32, 16),
            ("T{=i:foo:f:bar:10s:baz:}", 18, 1)]

        test_error_cases = [
            # sizeof(signed char) + padding is not a power of two.
            "T{<b:a:xxQ:b:}",
            # Missing padding bytes at the end of the struct.  The only
            # reason a compiler would add three padding bytes to field
            # zero is an artificial forced alignment of four for the short
            # in field one.  This in turn requires that the entire struct
            # has alignment four, which necessitates two padding bytes at
            # the end of the struct.
            "T{<b:a:xxxh:b:}",
            # Unnatural padding at the end of the struct (expect two padding
            # bytes instead of four).
            "T{<b:a:xxxh:b:xxxx}"]

        for fmt, itemsize, align in test_cases:
            t = ndt.from_format(fmt)
            self.assertEqual(t.itemsize, itemsize)
            self.assertEqual(t.align, align)

        for fmt in test_error_cases:
            self.assertRaises(ValueError, ndt.from_format, fmt)

    def test_fixed_bytes(self):
        for fmt in ['s', '100s']:
            t = ndt.from_format(fmt)
            s = struct.Struct(fmt)
            self.assertEqual(t.itemsize, s.size)

        # For consistency (it would be easy to allow, but other dtypes
        # cannot have size 0).
        self.assertRaises(ValueError, ndt.from_format, "0s")

        for fmt in ['0s', 's', '100s']:
            for modifier in ['@', '=', '<', '>', '!']:
                f = modifier + fmt
                self.assertRaises(ValueError, ndt.from_format, f)

    def test_primitive(self):
        standard = [
          '?',
          'c', 'b', 'B',
          'h', 'i', 'l', 'q',
          'H', 'I', 'L', 'Q',
          'f', 'd']

        native = ['n', 'N']

        if HAVE_PYTHON_36:
            standard += ['e']

        for fmt in standard:
            for modifier in ['', '@', '=', '<', '>', '!']:
                f = modifier + fmt
                t = ndt.from_format(f)
                s = struct.Struct(f)
                self.assertEqual(t.itemsize, s.size)

        for fmt in native:
            for modifier in ['', '@']:
                f = modifier + fmt
                t = ndt.from_format(f)
                s = struct.Struct(f)
                self.assertEqual(t.itemsize, s.size)

        for fmt in native:
            for modifier in ['=', '<', '>', '!']:
                f = modifier + fmt
                self.assertRaises(ValueError, ndt.from_format, f)
                self.assertRaises(struct.error, struct.Struct, f)

        if HAVE_PYTHON_36:
            # complex32
            fmt = 'Ze'
            for modifier in ['', '@', '=', '<', '>', '!']:
                f = modifier + fmt
                t = ndt.from_format(f)
                self.assertEqual(t.itemsize, 4)

        # complex64
        fmt = 'Zf'
        for modifier in ['', '@', '=', '<', '>', '!']:
            f = modifier + fmt
            t = ndt.from_format(f)
            self.assertEqual(t.itemsize, 8)

        # complex128
        fmt = 'Zd'
        for modifier in ['', '@', '=', '<', '>', '!']:
            f = modifier + fmt
            t = ndt.from_format(f)
            self.assertEqual(t.itemsize, 16)


class TestError(unittest.TestCase):

    def test_exceptions(self):
        self.assertRaises(TypeError, ndt, None)
        self.assertRaises(ValueError, ndt, "")
        self.assertRaises(ValueError, ndt, "xyz")
        self.assertRaises(ValueError, ndt, "var() * int64")


class TestConstruction(unittest.TestCase):

    def test_roundtrip(self):
        test_cases = [
            "2 * 3 * float64",
            "2 * 3 * {a : uint8, b : complex64}",
        ]
        for s in test_cases:
            t = ndt(s)
            self.assertEqual(str(t), s)

    def test_from_ndt(self):
        test_cases = [
          "2 * 3 * {a : 10 * bytes, b : 20 * string}",
          "var(offsets=[0,2]) * var(offsets=[0,3,10]) * complex128"]

        for s in test_cases:
            t = ndt(s)
            u = ndt(t)
            self.assertEqual(u, t)
            t = None
            gc.collect()

        t = ndt("{x: complex128, y: float64}", [[0, 2], [0, 3, 5]])
        u = ndt(t)
        self.assertEqual(u, t)
        t = None
        gc.collect()


class TestApply(unittest.TestCase):

    def test_apply(self):
        # Type checking and return type inference for function applications.

        # Function type:
        f = ndt("(Dims... * N * M * int64, Dims... * M * P * int64) -> Dims... * N * P * float64")

        # Argument types:
        args = ndt("(20 * 2 * 3 * int64, 20 * 3 * 4 * int64)")

        spec = f.apply(args)
        self.assertEqual(spec.func, f)
        self.assertEqual(spec.args, args)
        self.assertEqual(spec.ret, ndt("20 * 2 * 4 * float64"))
        self.assertEqual(spec.outer_dims, 1)

    def test_apply_error(self):

        f = ndt("(Dims... * N * M * int64, Dims... * M * P * int64) -> Dims... * N * P * float64")

        lst = ["(20 * 2 * 3 * int8, 20 * 3 * 4 * int64)",
               "(10 * 2 * 3 * int64, 20 * 3 * 4 * int64)",
               "(20 * 2 * 100 * int64, 20 * 3 * 4 * int64)"]

        for s in lst:
            args = ndt(s)
            self.assertRaises(TypeError, f.apply, args)

    def test_apply_overflow(self):

        if not HAVE_64_BIT:
            f = ndt("1073741824 * N * uint8 -> float64")
            arg = "1073741824 * 2 * uint8"
            self.assertRaises(MemoryError, f.apply, arg)


ALL_TESTS = [
  TestModule,
  TestFunction,
  TestVoid,
  TestAny,
  TestFixedDim,
  TestFortran,
  TestVarDim,
  TestSymbolicDim,
  TestEllipsisDim,
  TestTuple,
  TestRecord,
  TestRef,
  TestConstr,
  TestNominal,
  TestScalarKind,
  TestCategorical,
  TestFixedStringKind,
  TestFixedString,
  TestFixedBytesKind,
  TestFixedBytes,
  TestString,
  TestBytes,
  TestChar,
  TestBool,
  TestSignedKind,
  TestSigned,
  TestUnsignedKind,
  TestUnsigned,
  TestFloatKind,
  TestFloat,
  TestComplexKind,
  TestComplex,
  TestTypevar,
  TestCopy,
  TestBufferProtocol,
  TestConstruction,
  TestError,
  TestApply,
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--failfast", action="store_true",
                        help="stop the test run on first error")
    args = parser.parse_args()

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for case in ALL_TESTS:
        s = loader.loadTestsFromTestCase(case)
        suite.addTest(s)

    runner = unittest.TextTestRunner(failfast=args.failfast, verbosity=2)
    result = runner.run(suite)
    ret = not result.wasSuccessful()

    sys.exit(ret)
