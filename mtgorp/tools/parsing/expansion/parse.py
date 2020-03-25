from mtgorp.db.database import CardDatabase

from mtgorp.models.interfaces import Expansion

from mtgorp.tools.parsing.exceptions import ParseException


class ExpansionParseException(ParseException):
    pass


class ExpansionParser(object):

    def __init__(self, db: CardDatabase):
        self._db = db

    def _unique_expansion(self, s: str) -> Expansion:
        _s = s.lower()
        match = None
        for key, value in self._db.expansions.items():
            if _s in key.lower():
                if match is None:
                    match = value
                else:
                    raise ExpansionParseException(f'Soft expansion match not unique: "{s}" for {match} and {key}')

        if match is None:
            raise ExpansionParseException(f'Failed soft match for: "{s}"')

        return match

    def parse(self, s: str) -> Expansion:
        expansion = self._db.expansions.get(s.upper())
        return self._unique_expansion(s) if expansion is None else expansion