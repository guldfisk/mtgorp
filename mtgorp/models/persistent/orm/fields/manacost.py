from mtgorp.models.persistent.attributes.manacosts import ManaCost
from mtgorp.models.persistent.orm.fields.picklefield import PickleField


class ManaCostField(PickleField[ManaCost]):

    @property
    def python_type(self):
        return ManaCost
