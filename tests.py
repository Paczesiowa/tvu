from test_utils import TestCase

import tvu


class TVUTest(TestCase):

    def basic_test(self):
        class IntTVU(tvu.TVU):
            TYPES = int,

        @tvu(x=IntTVU)
        def foo(x):
            return x

        self.assertEqual(foo(1), 1)
        with self.assertRaises(TypeError, 'x must be int, not None'):
            foo(None)

    def two_types_test(self):
        class IntStrTVU(tvu.TVU):
            TYPES = int, str

        @tvu(x=IntStrTVU)
        def foo(x):
            pass

        foo(1)
        foo('a')
        with self.assertRaises(TypeError, 'x must be int or str, not None'):
            foo(None)

    def multiple_types_test(self):
        class IntStrListTVU(tvu.TVU):
            TYPES = int, str, list

        @tvu(x=IntStrListTVU)
        def foo(x):
            pass

        foo(1)
        foo('a')
        foo([])
        with self.assertRaises(TypeError,
                               'x must be int, str or list, not None'):
            foo(None)

    def multiple_validators_test(self):
        class IntTVU(tvu.TVU):
            TYPES = int,

        class StrTVU(tvu.TVU):
            TYPES = str,

        class FloatTVU(tvu.TVU):
            TYPES = float,

        @tvu(x=IntTVU, y=StrTVU, z=FloatTVU)
        def foo(x, y, z):
            pass

        foo(1, 'a', .0)

        with self.assertRaises(TypeError, 'x must be int, not 1'):
            foo('1', 'a', .0)
        with self.assertRaises(TypeError, 'y must be str, not 1'):
            foo(x=1, y=1, z=.0)
        with self.assertRaises(TypeError, 'z must be float, not 1.0'):
            foo(1, 'a', z='1.0')
