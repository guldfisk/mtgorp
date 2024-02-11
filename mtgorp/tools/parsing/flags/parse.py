import typing as t

from mtgorp.models.persistent.attributes.flags import Flag, Flags
from mtgorp.tools.parsing.exceptions import ParseException


class FlagsParseException(ParseException):
    pass


class FlagParser(object):
    card_type_map = {t.name.lower(): t for t in Flag}

    @classmethod
    def _unique_flag(cls, s: str) -> Flag:
        match = None
        for key, value in cls.card_type_map.items():
            if s in key:
                if match is None:
                    match = value
                else:
                    raise FlagsParseException(f'Soft flag match not unique: "{s}" for {match} and {key}')
        return match

    @classmethod
    def parse(cls, ss: t.Iterable[str]) -> Flags:
        for s in ss:
            flag = cls.card_type_map.get(s.lower())
            yield cls._unique_flag(s.lower()) if flag is None else flag
