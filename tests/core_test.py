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

    def missing_validator_test(self):
        class IntTVU(tvu.TVU):
            TYPES = int,

        @tvu(x=IntTVU)
        def foo(x, y):
            pass

        foo(1, 2)
        foo(2, y=3)
        with self.assertRaises(TypeError,
                               'x must be int, not None'):
            foo(None, None)

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

    def unification_test(self):
        class NumberTVU(tvu.TVU):
            TYPES = float, int

            def unify(self, value):
                if isinstance(value, int):
                    return float(value)
                else:
                    return value

        @tvu(x=NumberTVU)
        def foo(x):
            return x

        self.assertEqual(foo(1), 1.)
        self.assertTrue(isinstance(foo(1), float))
        self.assertEqual(foo(1.), 1.)
        self.assertTrue(isinstance(foo(1.), float))
        with self.assertRaises(TypeError,
                               'x must be float or int, not None'):
            foo(None)

    def validation_test(self):
        class PositiveIntTVU(tvu.TVU):
            TYPES = int,

            def validate(self, value):
                if value <= 0:
                    self.error(u'positive number')

        @tvu(x=PositiveIntTVU)
        def foo(x):
            pass

        foo(1)
        with self.assertRaises(TypeError, 'x must be int, not None'):
            foo(None)

        with self.assertRaises(ValueError,
                               'x must be positive number, not: 0'):
            foo(0)

        with self.assertRaises(ValueError,
                               'x must be positive number, not: -1'):
            foo(-1)
