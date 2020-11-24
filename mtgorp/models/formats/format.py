from __future__ import annotations

import itertools
import typing as t

from abc import ABCMeta, abstractmethod, ABC

from yeetlong.multiset import Multiset
from yeetlong.errors import Errors

from mtgorp.models.persistent.attributes.typeline import BASIC
from mtgorp.models.collections.deck import Deck


class _FormatMeta(ABCMeta):
    formats_map: t.MutableMapping[str, Format] = {}

    def __new__(mcs, classname, base_classes, attributes):
        klass = type.__new__(mcs, classname, base_classes, attributes)

        if 'name' in attributes:
            mcs.formats_map[attributes['name']] = klass

        return klass


class Validation(ABC):

    @abstractmethod
    def validate(self, deck: Deck) -> t.List[str]:
        pass


class DeckSizeIsMinimum(Validation):

    def __init__(self, size: int):
        self._expected_deck_size = size

    def validate(self, deck: Deck) -> t.List[str]:
        if len(deck.maindeck) < self._expected_deck_size:
            return [f'deck size {len(deck.maindeck)} below required minimum size {self._expected_deck_size}']
        return []


class DeckSizeIs(Validation):

    def __init__(self, size: int):
        self._expected_deck_size = size

    def validate(self, deck: Deck) -> t.List[str]:
        if len(deck.maindeck) != self._expected_deck_size:
            return [f'deck size {len(deck.maindeck)} does not match required {self._expected_deck_size}']
        return []


class SideboardSizeIs(Validation):

    def __init__(self, size: int):
        self._expected_sideboard_size = size

    def validate(self, deck: Deck) -> t.List[str]:
        if len(deck.sideboard) != self._expected_sideboard_size:
            return [f'sideboard size {len(deck.sideboard)} does not match required {self._expected_sideboard_size}']
        return []


class MaxDuplicates(Validation):

    def __init__(self, max_duplicates: int, ignore_basics: bool = True, respect_recommendations: bool = True):
        self._max_duplicates = max_duplicates
        self._ignore_basics = ignore_basics
        # TODO pretty sure mtgjson has something like this information
        self._respect_recommendations = respect_recommendations

    def validate(self, deck: Deck) -> t.List[str]:
        errors = []

        for cardboard, multiplicity in Multiset(
            printing.cardboard
            for printing in
            deck.seventy_five
            if not (self._ignore_basics and BASIC in printing.cardboard.front_card.type_line)
        ).items():
            if multiplicity > self._max_duplicates:
                errors.append(
                    'amount of {} ({}) greater than maximum allowed amount of single cardboard ({})'.format(
                        cardboard.name,
                        multiplicity,
                        self._max_duplicates,
                    )
                )

        return errors


class Format(object, metaclass = _FormatMeta):
    name: str
    validations: t.List[Validation] = []

    @classmethod
    def deckcheck(cls, deck: Deck) -> Errors:
        return Errors(
            list(
                itertools.chain(
                    *(
                        validation.validate(deck)
                        for validation in
                        cls.validations
                    )
                )
            )
        )


class Highlander(Format):
    name = 'highlander'
    validations = [
        DeckSizeIsMinimum(100),
        SideboardSizeIs(15),
        MaxDuplicates(1),
    ]


class Constructed(Format):
    name = 'constructed'
    validations = [
        DeckSizeIsMinimum(60),
        SideboardSizeIs(15),
        MaxDuplicates(4),
    ]


class Limited(Format):
    name = 'limited'
    validations = [
        DeckSizeIsMinimum(40)
    ]


class LimitedSideboard(Format):
    name = 'limited_sideboard'
    validations = [
        DeckSizeIsMinimum(40),
        SideboardSizeIs(15),
    ]


class Limited15Sideboard(Format):
    name = 'limited_15_sideboard'
    validations = [
        DeckSizeIs(15),
        SideboardSizeIs(7),
    ]
