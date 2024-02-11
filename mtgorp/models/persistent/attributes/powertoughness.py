from __future__ import annotations

import functools
import typing as t


@functools.total_ordering
class PTValue(object):
    def __init__(self, value: int = 0, variable: bool = False):
        self._value = value
        self._variable = variable

    @property
    def value(self) -> int:
        return 0 if self._variable else self._value

    @property
    def variable(self) -> bool:
        return self._variable

    def __repr__(self):
        return "*" if self._variable else str(self._value)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, self.__class__):
            if self._variable or other.variable:
                return self._variable and other.variable
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __gt__(self, other):
        return (
            isinstance(other, int)
            and self.value > other
            or isinstance(other, self.__class__)
            and self.value > other.value
        )

    def serialize(self) -> str:
        return repr(self)

    @classmethod
    def deserialize(cls, s: str) -> PTValue:
        return cls(0, variable=True) if s == "*" else cls(int(s))


class PowerToughness(object):
    def __init__(self, power: t.Union[int, PTValue], toughness: t.Union[int, PTValue]):
        self._power = power if isinstance(power, PTValue) else PTValue(power)
        self._toughness = toughness if isinstance(toughness, PTValue) else PTValue(toughness)

    @property
    def power(self) -> PTValue:
        return self._power

    @property
    def toughness(self) -> PTValue:
        return self._toughness

    def __eq__(self, other):
        return isinstance(other, PowerToughness) and self.power == other.power and self.toughness == other.toughness

    def __hash__(self):
        return hash((self.power, self.toughness))

    def __repr__(self):
        return "{}/{}".format(self.power, self.toughness)

    def __iter__(self):
        yield self.power
        yield self.toughness

    def serialize(self) -> str:
        return repr(self)

    @classmethod
    def deserialize(cls, s: str) -> PowerToughness:
        return cls(*(PTValue.deserialize(v) for v in s.split("/")))
