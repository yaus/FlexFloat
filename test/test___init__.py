from unittest import TestCase

from FlexFloat import FlexFloat


class TestFlexFloat(TestCase):
    def testFlexFloatFactory(self):
        x = FlexFloat[7, 11]
        q = x(0, 1, 1)
        print(q)

    def testAddition(self):
        x = FlexFloat[7, 11]
        a = x(1.5, 1, 1)
        b = x(2.5, 1, 1)
        result = a + b
        self.assertEqual(float(result), 4.0)

    def testSubtraction(self):
        x = FlexFloat[7, 11]
        a = x(5.5, 1, 1)
        b = x(2.5, 1, 1)
        result = a - b
        self.assertEqual(float(result), 3.0)

    def testMultiplication(self):
        x = FlexFloat[7, 11]
        a = x(3.0, 1, 1)
        b = x(2.0, 1, 1)
        result = a * b
        self.assertEqual(float(result), 6.0)

    def testDivision(self):
        x = FlexFloat[7, 11]
        a = x(10.0, 1, 1)
        b = x(2.0, 1, 1)
        result = a / b
        self.assertEqual(float(result), 5.0)