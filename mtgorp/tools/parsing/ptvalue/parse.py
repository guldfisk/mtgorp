import re

from mtgorp.models.persistent.attributes.powertoughness import PTValue
from mtgorp.tools.parsing.exceptions import ParseException


class PTValueParseException(ParseException):
    pass


class PTValueParser(object):
    matcher = re.compile("-?\\d+")

    @classmethod
    def parse(cls, s: str) -> PTValue:
        if not cls.matcher.match(s):
            if s == "*":
                return PTValue(variable=True)
            raise PTValueParseException()

        return PTValue(int(s))
