import functools
import typing as t

from enum import Enum


class Flag(Enum):
    TIMESHIFTED = 'timeshifted'
    DRAFT_MATTERS = 'draft_matters'


@functools.total_ordering
class Flags(object):

    def __init__(self, flags: t.Optional[t.Iterable[Flag]] = None):
        self._flags = frozenset() if flags is None else frozenset(flags)

    def __hash__(self) -> int:
        return self._flags.__hash__()

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self._flags == other._flags
        )

    def __contains__(self, item):
        if isinstance(item, self.__class__):
            return item._flags.issubset(self._flags)
        return item in self._flags

    def __iter__(self):
        return self._flags.__iter__()

    def __lt__(self, other):
        return (
            isinstance(other, self.__class__)
            and self._flags < other._flags
        )

    def __repr__(self):
        return f'{self.__class__.__name__}{tuple(flag.name for flag in self._flags)}'
