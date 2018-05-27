import typing as t

from mtgorp.models.persistent.attributes.typeline import TypeLine, ALL_TYPES, BaseCardType

from mtgorp.tools.parsing.exceptions import ParseException


class TypeParseException(ParseException):
	pass


class TypeLineParser(object):
	type_map = {
		t.name.lower(): t for t in ALL_TYPES
	}

	@classmethod
	def _unique_type(cls, s: str) -> BaseCardType:
		match = None
		for key, value in cls.type_map.items():
			if s in key:
				if match is None:
					match = value
				else:
					raise TypeParseException(f'Soft type match not unique: "{s}" for {match} and {key}')

		if match is None:
			raise TypeParseException(f'Failed soft match for: "{s}"')

		return match

	@classmethod
	def parse(cls, ss: t.Iterable[str]) -> TypeLine:
		types = []
		for s in ss:
			_type = cls.type_map.get(s.lower())
			types.append(cls._unique_type(s.lower()) if _type is None else _type)

		return TypeLine(types)