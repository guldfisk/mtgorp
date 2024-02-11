from sqlalchemy import types

from mtgorp.models.persistent.attributes.flags import Flag, Flags


class FlagsField(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: Flags, dialect) -> str:
        return ",".join(flag.name for flag in value)

    def process_result_value(self, value: str, dialect) -> Flags:
        if not value:
            return Flags()
        return Flags(Flag[color] for color in value.split(","))

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        return frozenset
