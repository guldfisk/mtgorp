import mtgorp.db.attributeparse.parser as parser
from mtgorp.db.attributeparse.exceptions import AttributeParseException
from mtgorp.models.persistent.attributes.rarities import Rarity


class RarityParseException(AttributeParseException):
    pass


class Parser(parser.Parser):
    _RARITY_MAP = {
        "common": Rarity.COMMON,
        "timeshifted common": Rarity.COMMON,
        "uncommon": Rarity.UNCOMMON,
        "timeshifted uncommon": Rarity.UNCOMMON,
        "rare": Rarity.RARE,
        "timeshifted rare": Rarity.RARE,
        "mythic": Rarity.MYTHIC,
        "basic Land": Rarity.LAND,
        "special": Rarity.SPECIAL,
    }

    @staticmethod
    def parse(s: str) -> Rarity:
        try:
            return Parser._RARITY_MAP[s]
        except KeyError:
            raise RarityParseException()
