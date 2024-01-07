from typing import ClassVar, Self, Type


class FlexFloat:
    from numbers import Number
    from ClassPropertyDescriptor import classproperty

    e_width: ClassVar[int] = 1
    m_width: ClassVar[int] = 1
    _m_one: ClassVar[int] = 2 ** m_width
    _class_storage: ClassVar[dict[int, dict[int, type["FlexFloat"]]]] = {}

    def __init__(self, s: int | bool, e: int, m: int):
        """
        Flexible Floating Point
        :param s: Sign
        :param e: Exponent
        :param m: Mantissa
        """
        if e <= 0 or m <= 0:
            raise ValueError(f'e or m must be nature number')
        if e.bit_length() > self.e_width:
            raise ValueError(f'Bit width of e must <= {self.e_width}')
        if m.bit_length() > self.m_width:
            raise ValueError(f'Bit width of m must <= {self.m_width}')
        self._s = s != 0
        self._e = e
        self._m = m

    @property
    def s(self) -> bool:
        """
        Sign
        :return:
        """
        return self._s

    @property
    def e(self) -> int:
        """
        Exponent
        :return:
        """
        return self._e

    @property
    def m(self) -> int:
        """
        Mantissa
        :return:
        """
        return self._m

    def __class_getitem__(cls, item: tuple[int, int] | tuple[int, int, bool]) -> type["FlexFloat"]:
        """
        Return a class object with specified width for exponent and mantissa
        :param item: (e_width, m_width) or (e_width, m_width, denormal)
        :return: FlexFloat class object
        """
        e, m, *d = item
        if e <= 0 or m <= 0:
            raise ValueError(f'[e,m]: e or m must be nature number')
        if d is None:
            d = False

        _e = FlexFloat._class_storage.setdefault(e, {})

        if m not in _e:
            # Reuse
            class FlexFloatEM(FlexFloat):
                e_width, m_width = e, m
                _m_one = 2 ** m

            FlexFloatEM.__qualname__ = f"FlexFloat[{e},{m}]"
            _class_obj = FlexFloatEM
            _e[m] = _class_obj

        return _e[m]

    @classproperty
    def exponent_offset(cls):
        """
        Offset of exponent
        :return:
        """
        return 2 ** (cls.e_width - 1) - 1

    def _add_(self, other: Self) -> Self:
        delta = self._e - other._m
        if delta > 0:
            s_m = self._m_one + self._m
            o_m = (self._m_one + other._m) >> delta
        else:
            s_m = (self._m_one + self._m) >> -delta
            o_m = self._m_one + other._m

        match (self.s != other.s, self.s, s_m > o_m):
            case False, _, _:
                _s = self.s
                _m = s_m + o_m
                _o = _m >= (self._m_one * 2)
                _e = (self._e if delta > 0 else other._e) + _o
            case True, False, True:
                _s = False
                _m = s_m - o_m
                # _e = (self._e if delta)
        return self.__class__(_s, _e, _m)

    def __add__(self, other: Number | Self) -> Self:
        if isinstance(other, FlexFloat):
            if self.compatible(other):
                return self._add_(other)

    def __repr__(self):
        sign_str = '-' if self.s else '+'
        m_str = f"{(self._m / self._m_one): 1.10f}"
        if self.is_zero():
            return f"{sign_str}{0}.{0}"
        else:
            return f"{sign_str}{1}.{m_str[3:]}*2^{self._e - self.exponent_offset}"
        return

    def compatible(self, other):
        """
        Check compatibility of two FlexFloat
        :param other: FlexFloat
        :return: compatible or not
        """
        return self.m_width == other.m_width and self.e_width == other.e_width


    def is_zero(self):
        """
        Check if the number is zero
        :return:
        """
        return self._e == 0 and self._m == 0
