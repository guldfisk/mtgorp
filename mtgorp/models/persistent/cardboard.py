from __future__ import annotations

import typing as t
from itertools import chain

from orp.database import Model, PrimaryKey, Key
from orp.relationships import Many, ListMany

from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.interfaces import Card, Expansion, Printing, Block
from mtgorp.models.interfaces import Side as _Side
from mtgorp.models.interfaces import Cardboard as _Cardboard


class Side(_Side):

    def __init__(self, owner: Cardboard):
        self._owner = owner
        self._cards = ListMany(
            self,
            '_sides',
        )

    @property
    def owner(self) -> Cardboard:
        return self._owner

    @property
    def cards(self) -> ListMany[Card]:
        return self._cards


class Cardboard(Model, _Cardboard):
    primary_key = PrimaryKey(
        Key(
            'name',
            calc_value = lambda k, o, m: o.__class__.calc_name(
                c.name
                for c in
                (
                    chain(m['front_cards'], m['back_cards'])
                    if m['back_cards'] is not None else
                    m['front_cards']
                )
            ),
            input_values = ('front_cards', 'back_cards'),
        )
    )    
    _SPLIT_SEPARATOR = ' // '

    _name: str
    _cards = t.Tuple[Card, ...]

    def __init__(
        self,
        front_cards: t.Tuple[Card, ...],
        back_cards: t.Tuple[Card, ...] = None,
        layout: Layout = Layout.STANDARD,
    ):
        self._front_cards = Side(self)

        for c in front_cards:
            self._front_cards.cards.add(c)

        self._back_cards = Side(self)

        if back_cards is not None:
            for c in back_cards:
                self._back_cards.cards.add(c)

        self._layout = layout

        self._printings: Many[Printing] = Many(self, '_cardboard')

        self._cards = None

    @classmethod
    def calc_name(cls, names) -> str:
        return cls._SPLIT_SEPARATOR.join(names)

    @property
    def name(self) -> str:
        return self._name

    @property
    def printings(self) -> Many[Printing]:
        return self._printings

    @property
    def expansions(self) -> t.Iterable[Expansion]:
        return (printing.expansion for printing in self._printings)

    @property
    def front_cards(self) -> ListMany[Card]:
        return self._front_cards.cards

    @property
    def back_cards(self) -> ListMany[Card]:
        return self._back_cards.cards

    @property
    def cards(self) -> t.Tuple[Card, ...]:
        if self._cards is None:
            self._cards = tuple(self.front_cards) + tuple(self.back_cards)

        return self._cards

    @property
    def layout(self) -> Layout:
        return self._layout

    @property
    def front_card(self) -> Card:
        return self._front_cards.cards.__iter__().__next__()

    @property
    def back_card(self) -> t.Optional[Card]:
        try:
            return self._back_cards.cards._many[0]
        except IndexError:
            return None

    @property
    def printing(self) -> Printing:
        return self.printings.__iter__().__next__()

    def from_expansion(self, expansion: t.Union[Expansion, str], allow_volatile: t.Optional[bool] = False) -> Printing:
        if allow_volatile:
            if isinstance(expansion, Expansion):
                for printing in self.printings:
                    if printing.expansion == expansion:
                        return printing
            else:
                for printing in self.printings:
                    if printing.expansion.code == expansion:
                        return printing
        else:
            options = []
            if isinstance(expansion, Expansion):
                for printing in self.printings:
                    if printing.expansion == expansion:
                        options.append(printing)
            else:
                for printing in self.printings:
                    if printing.expansion.code == expansion:
                        options.append(printing)

            if len(options) > 1:
                raise RuntimeError(
                    f'{self} printed multiple times in {expansion}'
                )

            if options:
                return options[0]

        raise KeyError(
            '{} not printed in {}'.format(
                self,
                expansion,
            )
        )

    def from_block(self, block: t.Union[Block, str]) -> Printing:
        if isinstance(block, Block):
            for printing in self.printings:
                if printing.expansion.block == block:
                    return printing
        else:
            for printing in self.printings:
                if printing.expansion.block is not None and printing.expansion.block.name == block:
                    return printing

        raise KeyError(
            '{} not printed in {}'.format(
                self,
                block,
            )
        )

    @property
    def original_printing(self) -> Printing:
        return sorted(
            self._printings,
            key = lambda printing:
            printing.expansion.release_date
        )[0]
