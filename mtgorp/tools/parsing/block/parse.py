from mtgorp.db.database import CardDatabase

from mtgorp.models.interfaces import Block

from mtgorp.tools.parsing.exceptions import ParseException


class BlockParseException(ParseException):
    pass


class BlockParser(object):

    def __init__(self, db: CardDatabase):
        self._db = db

    def _unique_block(self, s: str) -> Block:
        _s = s.lower()
        match = None
        for key, value in self._db.blocks.items():
            if _s in key.lower():
                if match is None:
                    match = value
                else:
                    raise BlockParseException(f'Soft block match not unique: "{s}" for {match} and {key}')

        if match is None:
            raise BlockParseException(f'Failed soft match for: "{s}"')

        return match

    def parse(self, s: str) -> Block:
        block = self._db.blocks.get(s.lower().capitalize())
        return self._unique_block(s) if block is None else block