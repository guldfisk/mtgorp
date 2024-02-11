import typing as t

from sqlalchemy import types


class FragmentDividersField(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: t.Optional[t.Sequence[int]], dialect) -> t.Optional[str]:
        if value is None:
            return None
        return ",".join(map(str, value))

    def process_result_value(self, value: t.Optional[str], dialect) -> t.Optional[t.Sequence[int]]:
        if not value:
            return None
        return tuple(map(int, value.split(",")))

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        return tuple
