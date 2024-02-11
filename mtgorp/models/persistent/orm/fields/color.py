import typing as t

from sqlalchemy import types

from mtgorp.models.persistent.attributes.colors import Color


class ColorField(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: t.Optional[t.FrozenSet[Color]], dialect) -> t.Optional[str]:
        if value is None:
            return None
        return ",".join(color.name for color in value)

    def process_result_value(self, value: t.Optional[str], dialect) -> t.FrozenSet[Color]:
        if not value:
            return frozenset()
        return frozenset(Color[color] for color in value.split(","))

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        return frozenset
