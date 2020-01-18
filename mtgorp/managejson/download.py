import typing as t

import os
import requests as r

import mtgorp.managejson.paths as paths


def download_file(url: str, location: str, chunk_size: int = 1024) -> None:
    ro = r.get(url, stream = True)
    with open(location, 'wb') as f:
        for chunk in ro.iter_content(chunk_size = chunk_size):
            f.write(chunk)


TO_RETRIEVE = {
    paths.ALL_CARDS_PATH: 'http://mtgjson.com/json/AllCards.json',
    paths.ALL_SETS_PATH: 'http://mtgjson.com/json/AllSets.json'
}


def make_new(to_retrieve: t.Mapping[str, str]) -> None:
    for path in to_retrieve:
        download_file(
            to_retrieve[path],
            path,
        )


def re_download() -> None:
    if not os.path.exists(paths.JSON_PATH):
        os.makedirs(paths.JSON_PATH)
    make_new(TO_RETRIEVE)


if __name__ == '__main__':
    re_download()
