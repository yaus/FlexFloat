from unittest import TestCase

from FlexFloat import FlexFloat


class TestFlexFloat(TestCase):
    def testFlexFloatFactory(self):
        x = FlexFloat[7, 11]
        q = x(0, 12, 12)

        print(q)
