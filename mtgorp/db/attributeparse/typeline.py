import re

import mtgorp.db.attributeparse.parser as parser
from mtgorp.db.attributeparse.exceptions import AttributeParseException
from mtgorp.models.persistent.attributes.typeline import ALL_TYPES, TRIBAL, TypeLine


class CardTypeParseException(AttributeParseException):
    pass


class Parser(parser.Parser):
    card_type_map = {"Kindred": TRIBAL, **{t.name: t for t in ALL_TYPES}}
    type_matcher = re.compile("[\\w\\-’]+")

    @staticmethod
    def parse(s: str) -> TypeLine:
        try:
            return TypeLine(
                *(Parser.card_type_map[m.group()] for m in Parser.type_matcher.finditer(s.replace("'", "’")))
            )
        except KeyError as e:
            raise CardTypeParseException(e)
