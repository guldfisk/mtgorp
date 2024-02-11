from __future__ import annotations

import typing as t
from itertools import chain

from orp.models import Key, Model, PrimaryKey
from orp.relationships import ListMany, Many

from mtgorp.models.interfaces import Card
from mtgorp.models.interfaces import Cardboard as _Cardboard
from mtgorp.models.interfaces import Printing
from mtgorp.models.interfaces import Side as _Side
from mtgorp.models.persistent.attributes.layout import Layout


class Side(_Side):
    def __init__(self, owner: Cardboard):
        self._owner = owner
        self._cards = ListMany(
            self,
            "_sides",
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
            "name",
            calc_value=lambda k, o, m: o.__class__.calc_name(
                c.name
                for c in (
                    chain(m["front_cards"], m["back_cards"]) if m["back_cards"] is not None else m["front_cards"]
                )
            ),
            input_values=("front_cards", "back_cards"),
        )
    )

    _name: str

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

        self._printings: Many[Printing] = Many(self, "_cardboard")

        self._cards = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def printings(self) -> Many[Printing]:
        return self._printings

    @property
    def front_cards(self) -> ListMany[Card]:
        return self._front_cards.cards

    @property
    def back_cards(self) -> ListMany[Card]:
        return self._back_cards.cards

    @property
    def layout(self) -> Layout:
        return self._layout
