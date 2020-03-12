import mtgorp.db.attributeparse.parser as parser

from mtgorp.models.persistent.attributes.expansiontype import ExpansionType


class Parser(parser.Parser):
    _EXPANSION_TYPE_MAP = {
        'core': ExpansionType.SET,
        'expansion': ExpansionType.SET,
        'funny': ExpansionType.FUNNY,
    }

    @classmethod
    def parse(cls, s: str) -> ExpansionType:
        return cls._EXPANSION_TYPE_MAP.get(s, ExpansionType.OTHER)
