import os

import appdirs

APP_DATA_PATH = appdirs.AppDirs('mtgorp', 'mtgorp').user_data_dir
JSON_PATH = os.path.join(APP_DATA_PATH, 'jsons')
ALL_CARDS_PATH = os.path.join(JSON_PATH, 'allCards' + '.json')
ALL_SETS_PATH = os.path.join(JSON_PATH, 'allSets' + '.json')
