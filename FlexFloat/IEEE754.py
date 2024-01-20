from . import FlexFloat


class IEEE754FlexFloat(FlexFloat):
    """
    A class that represents IEEE754 compatible floating point numbers.
    """
    pass


class IEEE754Single(IEEE754FlexFloat):
    """
    A class that represents IEEE754 single-precision floating point numbers.
    """
    e_width = 8
    m_width = 23


class IEEE754Double(IEEE754FlexFloat):
    """
    A class that represents IEEE754 double-precision floating point numbers.
    """
    e_width = 11
    m_width = 52
