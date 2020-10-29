import typing as t

from mtgorp.models.interfaces import BoosterKey
from mtgorp.models.persistent.orm.fields.picklefield import PickleField


class BoosterKeyField(PickleField[t.FrozenSet[BoosterKey]]):

    @property
    def python_type(self):
        return BoosterKey
