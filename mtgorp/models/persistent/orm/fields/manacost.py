import typing as t

from sqlalchemy import types

from mtgorp.models.persistent.attributes.manacosts import ManaCost


class ManaCostField(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: ManaCost, dialect) -> t.Optional[str]:
        if value is None:
            return None
        return str(value)

    def process_result_value(self, value: t.Optional[str], dialect) -> t.Optional[ManaCost]:
        if not value:
            return None
        return ManaCost.deserialize(value)

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        return ManaCost
