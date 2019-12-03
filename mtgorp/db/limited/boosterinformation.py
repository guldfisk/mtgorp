import os
import json


DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    'data.json'
)


class BoosterInformation(object):
    _data = dict()

    @staticmethod
    def information():
        if not BoosterInformation._data:
            with open(DATA_PATH, 'r') as f:
                BoosterInformation._data = json.load(f)
        return BoosterInformation._data
