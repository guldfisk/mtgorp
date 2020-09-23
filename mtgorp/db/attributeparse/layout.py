import mtgorp.db.attributeparse.parser as parser

from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.db.attributeparse.exceptions import AttributeParseException


class LayoutParseException(AttributeParseException):
    pass


class Parser(parser.Parser):
    _LAYOUT_MAP = {
        'normal': Layout.STANDARD,
        'leveler': Layout.STANDARD,
        'transform': Layout.TRANSFORM,
        'flip': Layout.FLIP,
        'meld': Layout.MELD,
        'split': Layout.SPLIT,
        'aftermath': Layout.AFTERMATH,
        'saga': Layout.SAGA,
        'adventure': Layout.ADVENTURE,
        'modal_dfc': Layout.MODAL,
    }

    @classmethod
    def parse(cls, s: str) -> Layout:
        try:
            return cls._LAYOUT_MAP[s]

        except KeyError:
            raise LayoutParseException(f'Invalid layout "{s}"')
