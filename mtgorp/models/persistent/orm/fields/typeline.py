import sqlalchemy.types as types

from mtgorp.models.persistent.attributes.typeline import ALL_TYPES_MAP, TypeLine


class TypeLineField(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: TypeLine, dialect):
        return str(value)

    def process_result_value(self, value: str, dialect):
        return TypeLine(*(ALL_TYPES_MAP[_t] for _t in value.split(" ") if _t != "—"))

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        return TypeLine
