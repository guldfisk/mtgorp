from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.tools.parsing.exceptions import ParseException


class RarityParseException(ParseException):
    pass


class RarityParser(object):
    rarity_map = {t.name.lower(): t for t in Rarity}

    @classmethod
    def _unique_rarity(cls, s: str) -> Rarity:
        match = None
        for key, value in cls.rarity_map.items():
            if s in key:
                if match is None:
                    match = value
                else:
                    raise RarityParseException(f'Soft rarity match not unique: "{s}" for {match} and {key}')

        if match is None:
            raise RarityParseException(f'Failed soft match for: "{s}"')

        return match

    @classmethod
    def parse(cls, s: str) -> Rarity:
        _s = s.lower()
        rarity = cls.rarity_map.get(_s)
        return cls._unique_rarity(_s) if rarity is None else rarity
