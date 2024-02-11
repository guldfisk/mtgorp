from __future__ import annotations

import io
import re
import typing as t
from abc import ABCMeta, abstractmethod
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from yeetlong.multiset import BaseMultiset, Multiset

from mtgorp.db.database import CardDatabase
from mtgorp.models.collections.deck import Deck
from mtgorp.models.interfaces import Printing
from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.serilization.serializeable import SerializationException
from mtgorp.models.serilization.strategies.jsonid import JsonId
from mtgorp.tools.groupification.groupification import (
    STANDARD_PRINTING_GROUPIFYER,
    Group,
    Groupifyer,
)


class _TabModelSerializerMeta(ABCMeta):
    extension_to_serializer: t.Mapping[str, t.Type[DeckSerializer]] = {}

    def __new__(mcs, classname, base_classes, attributes):
        klass = type.__new__(mcs, classname, base_classes, attributes)

        if "extensions" in attributes:
            for extension in attributes["extensions"]:
                mcs.extension_to_serializer[extension] = klass

        return klass


class DeckSerializer(object, metaclass=_TabModelSerializerMeta):
    extensions: t.Sequence[str]

    def __init__(self, db: CardDatabase, **kwargs):
        self._db = db

    @abstractmethod
    def serialize(self, tab_model: Deck) -> t.AnyStr:
        pass

    @abstractmethod
    def deserialize(self, s: t.AnyStr) -> Deck:
        pass


class DecSerializer(DeckSerializer):
    extensions = ["dec", "mwDeck"]

    def __init__(
        self,
        db: CardDatabase,
        *,
        include_header: bool = True,
        groupifyer: t.Optional[Groupifyer[Printing]] = STANDARD_PRINTING_GROUPIFYER,
        sideboard_groupifyer: t.Optional[Groupifyer[Printing]] = None,
        sideboard_indicator: str = "SB: ",
        allow_volatile_printing_load: bool = True,
    ):
        super().__init__(db)
        self._include_header = include_header
        self._groupifyer = groupifyer
        self._sideboard_groupifyer = sideboard_groupifyer
        self._sideboard_indicator = sideboard_indicator
        self._allow_volatile_printing_load = allow_volatile_printing_load

    def _printings_to_line(self, printing: Printing, multiplicity: int, sideboard: bool = False) -> str:
        return "{}{} [{}] {}".format(
            self._sideboard_indicator if sideboard else "",
            multiplicity,
            printing.expansion.code,
            printing.cardboard.name.replace("//", "/"),
        )

    def _printings_to_lines(self, printings: BaseMultiset[Printing], sideboard: bool = False) -> str:
        return "\n".join(
            self._printings_to_line(printing, multiplicity, sideboard)
            for printing, multiplicity in sorted(
                printings.items(),
                key=lambda p: (p[0].cardboard.name, p[0].expansion.code),
            )
        )

    def _block_from_group(self, group: Group[Printing], sideboard: bool = False) -> str:
        printings = Multiset(group.items)
        return "// {} ({})\n{}".format(
            (self._sideboard_indicator if sideboard else "") + group.name,
            len(printings),
            self._printings_to_lines(printings, sideboard=sideboard),
        )

    @classmethod
    def _get_header(cls, deck: Deck):
        return "// Maindeck: {}, Sideboard: {}\n\n".format(
            len(deck.maindeck),
            len(deck.sideboard),
        )

    def serialize(self, deck: Deck) -> t.AnyStr:
        s = ""
        if self._include_header:
            s += self._get_header(deck)
        if self._groupifyer is None:
            s += self._printings_to_lines(deck.maindeck)
        else:
            s += "\n\n".join(
                self._block_from_group(group) for group in self._groupifyer.groupify(deck.maindeck).groups
            )

        if deck.sideboard:
            if self._sideboard_groupifyer is None:
                s += "\n\n" + self._printings_to_lines(deck.sideboard, sideboard=True)
            else:
                s += "\n\n".join(
                    self._block_from_group(group, sideboard=True)
                    for group in self._sideboard_groupifyer.groupify(deck.sideboard).groups
                )

        return s

    def _get_printing(self, name: str, expansion_code: str) -> Printing:
        try:
            try:
                cardboard = self._db.cardboards[name]
            except KeyError:
                cardboard = self._db.cards[name].cardboard
        except KeyError:
            raise SerializationException('invalid cardboard name "{}"'.format(name))
        try:
            return cardboard.from_expansion(expansion_code, allow_volatile=True)
        except KeyError:
            if self._allow_volatile_printing_load:
                return cardboard.latest_printing
            raise SerializationException(
                'invalid expansion "{}" for cardboard "{}"'.format(expansion_code, cardboard.name)
            )

    def deserialize(self, s: t.AnyStr) -> Deck:
        maindeck = Multiset()
        sideboard = Multiset()
        pattern = re.compile(r"({}\s+)?(\d+) \[([A-Z0-9]*)\] (.*?)\s*$".format(self._sideboard_indicator.rstrip()))
        for ln in s.split("\n"):
            m = pattern.match(ln)
            if m:
                is_sideboard, qty, expansion, name = m.groups()
                (sideboard if is_sideboard else maindeck).add(
                    self._get_printing(name.replace("/", "//"), expansion),
                    int(qty),
                )

        return Deck(
            maindeck,
            sideboard,
        )


class JsonSerializer(DeckSerializer):
    extensions = ["json", "JSON"]

    def serialize(self, deck: Deck) -> t.AnyStr:
        return JsonId.serialize(deck)

    def deserialize(self, s: t.AnyStr) -> Deck:
        return JsonId(self._db).deserialize(Deck, s)


class CodSerializer(DeckSerializer):
    extensions = ["cod"]

    def serialize(self, deck: Deck) -> t.AnyStr:
        root = ElementTree.Element("cockatrice_deck", {"version": "1"})
        ElementTree.SubElement(root, "decknames")
        ElementTree.SubElement(root, "comments")
        maindeck = ElementTree.SubElement(root, "zone", {"name": "main"})
        sideboard = ElementTree.SubElement(root, "zone", {"name": "side"})

        for element, printings in ((maindeck, deck.maindeck), (sideboard, deck.sideboard)):
            for cardboard, multiplicity in Multiset(printing.cardboard for printing in printings).items():
                ElementTree.SubElement(
                    element,
                    "card",
                    {
                        "number": str(multiplicity),
                        "price": "0",
                        "name": (
                            cardboard.front_card.name
                            if cardboard.layout == Layout.FLIP
                            else " // ".join(card.name for card in cardboard.front_cards)
                        ),
                    },
                )

        with io.BytesIO() as f:
            ElementTree.ElementTree(root).write(f, encoding="utf-8", xml_declaration=True)
            return f.getvalue()

    def _element_to_printings(self, element: Element) -> t.Tuple[Printing, int]:
        try:
            printing = self._db.cardboards[element.attrib["name"]].latest_printing
        except KeyError:
            try:
                printing = self._db.cards[element.attrib["name"]].cardboards.__iter__().__next__().latest_printing
            except KeyError:
                raise SerializationException('unknown cardboard "{}"'.format(element.attrib.get("name")))
        try:
            multiplicity = int(element.attrib.get("number", 1))
        except ValueError:
            raise SerializationException('unknown quantity "{}"'.format(element.attrib.get("number")))

        return printing, multiplicity

    def deserialize(self, s: t.AnyStr) -> Deck:
        root = ElementTree.fromstring(s)
        return Deck(
            (
                (printing, multiplicity)
                for printing, multiplicity in map(
                    self._element_to_printings,
                    root.findall('zone[@name="main"]/card'),
                )
            ),
            (
                (printing, multiplicity)
                for printing, multiplicity in map(
                    self._element_to_printings,
                    root.findall('zone[@name="side"]/card'),
                )
            ),
        )
