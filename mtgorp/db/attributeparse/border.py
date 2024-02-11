import mtgorp.db.attributeparse.parser as parser
from mtgorp.db.attributeparse.exceptions import AttributeParseException
from mtgorp.models.persistent.attributes.borders import Border


class BorderParseException(AttributeParseException):
    pass


class Parser(parser.Parser):
    _BORDER_MAP = {
        "black": Border.BLACK,
        "white": Border.WHITE,
        "silver": Border.SILVER,
    }

    @staticmethod
    def parse(s: str) -> Border:
        try:
            return Parser._BORDER_MAP[s]
        except KeyError:
            raise BorderParseException()
