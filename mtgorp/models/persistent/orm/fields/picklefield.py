import pickle
import typing as t
from abc import abstractmethod

import sqlalchemy.types as types


T = t.TypeVar("T")


class PickleField(types.TypeDecorator, t.Generic[T]):
    impl = types.LargeBinary

    def process_bind_param(self, value: T, dialect) -> bytes:
        return pickle.dumps(value)

    def process_result_value(self, value: bytes, dialect) -> T:
        return pickle.loads(value)

    def process_literal_param(self, value, dialect):
        pass

    @property
    @abstractmethod
    def python_type(self):
        pass
