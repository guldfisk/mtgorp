from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.tools.parsing.exceptions import ParseException


class LayoutParseException(ParseException):
    pass


class LayoutParser(object):
    layout_map = {t.name.lower(): t for t in Layout}

    @classmethod
    def _unique_rarity(cls, s: str) -> Layout:
        match = None
        for key, value in cls.layout_map.items():
            if s in key:
                if match is None:
                    match = value
                else:
                    raise LayoutParseException(f'Soft layout match not unique: "{s}" for {match} and {key}')

        if match is None:
            raise LayoutParseException(f'Failed soft match for: "{s}"')

        return match

    @classmethod
    def parse(cls, s: str) -> Layout:
        _s = s.lower()
        layout = cls.layout_map.get(_s)
        return cls._unique_rarity(_s) if layout is None else layout
