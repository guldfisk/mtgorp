import typing as t

from sqlalchemy import types

from mtgorp.models.persistent.attributes.powertoughness import PowerToughness, PTValue


class PTValueField(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: t.Optional[PTValue], dialect) -> t.Optional[str]:
        if value is None:
            return None
        return value.serialize()

    def process_result_value(self, value: t.Optional[str], dialect) -> t.Optional[PTValue]:
        if value is None:
            return None
        return PTValue.deserialize(value)

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        return PTValue


class PowerToughnessField(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: t.Optional[PowerToughness], dialect) -> t.Optional[str]:
        if value is None:
            return None
        return value.serialize()

    def process_result_value(self, value: t.Optional[str], dialect) -> t.Optional[PowerToughness]:
        if value is None:
            return None
        return PowerToughness.deserialize(value)

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        return PowerToughness
