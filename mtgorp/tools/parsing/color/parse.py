import typing as t

from mtgorp.models.interfaces import Color
from mtgorp.tools.parsing.exceptions import ParseException


class ColorParseException(ParseException):
    pass


class ColorParse(object):
    _COLOR_MAP = {color.letter_code: color for color in Color}

    @classmethod
    def parse(cls, s: str) -> t.AbstractSet[Color]:
        try:
            return frozenset(cls._COLOR_MAP[c.upper()] for c in s)
        except KeyError:
            raise ColorParseException()
