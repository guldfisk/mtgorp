import typing as t

from abc import ABCMeta, abstractmethod

from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.flags import Flags
from mtgorp.models.persistent.attributes.typeline import TypeLine
from mtgorp.models.persistent.attributes.manacosts import ManaCost
from mtgorp.models.persistent.attributes.colors import Color
from mtgorp.models.persistent.attributes.powertoughness import PTValue
from mtgorp.models.persistent.expansion import Expansion
from mtgorp.models.persistent.block import Block
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.printing import Printing


T = t.TypeVar('T')


class ExtractionStrategy(t.Generic[T], metaclass = ABCMeta):

    @classmethod
    @abstractmethod
    def extract_name(cls, extractable: T) -> t.Iterable[str]:
        pass

    @classmethod
    @abstractmethod
    def extract_layout(cls, extractable: T) -> t.Iterable[Layout]:
        pass

    @classmethod
    @abstractmethod
    def extract_cmc(cls, extractable: T) -> t.Iterable[int]:
        pass

    @classmethod
    @abstractmethod
    def extract_rarity(cls, extractable: T) -> t.Iterable[Rarity]:
        pass

    @classmethod
    @abstractmethod
    def extract_flags(cls, extractable: T) -> t.Iterable[Flags]:
        pass

    @classmethod
    @abstractmethod
    def extract_type_line(cls, extractable: T) -> t.Iterable[TypeLine]:
        pass

    @classmethod
    @abstractmethod
    def extract_mana_cost(cls, extractable: T) -> t.Iterable[ManaCost]:
        pass

    @classmethod
    @abstractmethod
    def extract_color(cls, extractable: T) -> t.Iterable[t.AbstractSet[Color]]:
        pass

    @classmethod
    @abstractmethod
    def extract_colors(cls, extractable: T) -> t.Iterable[t.AbstractSet[Color]]:
        pass

    @classmethod
    @abstractmethod
    def extract_oracle(cls, extractable: T) -> t.Iterable[str]:
        pass

    @classmethod
    @abstractmethod
    def extract_flavor(cls, extractable: T) -> t.Iterable[str]:
        pass

    @classmethod
    @abstractmethod
    def extract_power(cls, extractable: T) -> t.Iterable[PTValue]:
        pass

    @classmethod
    @abstractmethod
    def extract_toughness(cls, extractable: T) -> t.Iterable[PTValue]:
        pass

    @classmethod
    @abstractmethod
    def extract_loyalty(cls, extractable: T) -> t.Iterable[PTValue]:
        pass

    @classmethod
    @abstractmethod
    def extract_artist(cls, extractable: T) -> t.Iterable[str]:
        pass

    @classmethod
    @abstractmethod
    def extract_expansion(cls, extractable: T) -> t.Iterable[Expansion]:
        pass

    @classmethod
    @abstractmethod
    def extract_block(cls, extractable: T) -> t.Iterable[Block]:
        pass


class Extractor(t.Generic[T], metaclass = ABCMeta):
    extraction_type = None

    @classmethod
    @abstractmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[T]:
        pass

    @classmethod
    @abstractmethod
    def explain(cls) -> str:
        pass


class NameExtractor(Extractor[str]):
    extraction_type = str

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[str]:
        return strategy.extract_name(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'name'


class LayoutExtractor(Extractor[Layout]):
    extraction_type = Layout

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[Layout]:
        return strategy.extract_layout(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'layout'


class CmcExtractor(Extractor[int]):
    extraction_type = int

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[int]:
        return strategy.extract_cmc(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'cmc'


class RarityExtractor(Extractor[Rarity]):
    extraction_type = Rarity

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[Rarity]:
        return strategy.extract_rarity(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'rarity'


class FlagsExtractor(Extractor[Flags]):
    extraction_type = Flags

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[Flags]:
        return strategy.extract_flags(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'flags'


class TypeLineExtractor(Extractor[TypeLine]):
    extraction_type = TypeLine

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[TypeLine]:
        return strategy.extract_type_line(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'type line'


class ManaCostExtractor(Extractor[ManaCost]):
    extraction_type = ManaCost

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[ManaCost]:
        return strategy.extract_mana_cost(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'mana cost'


class ColorExtractor(Extractor[t.AbstractSet[Color]]):
    extraction_type = t.AbstractSet[Color]

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[t.AbstractSet[Color]]:
        return strategy.extract_colors(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'colors'


class OracleExtractor(Extractor[str]):
    extraction_type = str

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[str]:
        return strategy.extract_oracle(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'oracle text'


class FlavorExtractor(Extractor[str]):
    extraction_type = str

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[str]:
        return strategy.extract_flavor(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'flavor text'


class PowerExtractor(Extractor[PTValue]):
    extraction_type = PTValue

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[PTValue]:
        return strategy.extract_power(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'power'


class ToughnessExtractor(Extractor[PTValue]):
    extraction_type = PTValue

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[PTValue]:
        return strategy.extract_toughness(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'toughness'


class LoyaltyExtractor(Extractor[PTValue]):
    extraction_type = PTValue

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[PTValue]:
        return strategy.extract_loyalty(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'loyalty'


class ArtistExtractor(Extractor[str]):
    extraction_type = str

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[str]:
        return strategy.extract_artist(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'artist name'


class ExpansionExtractor(Extractor[Expansion]):
    extraction_type = Expansion

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[Expansion]:
        return strategy.extract_expansion(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'expansion'


class BlockExtractor(Extractor[Block]):
    extraction_type = Block

    @classmethod
    def extract(cls, extractable: t.Any, strategy: t.Type[ExtractionStrategy]) -> t.Iterable[Block]:
        return strategy.extract_block(extractable)

    @classmethod
    def explain(cls) -> str:
        return 'block'


class CardboardStrategy(ExtractionStrategy[Cardboard]):

    @classmethod
    def extract_name(cls, cardboard: Cardboard) -> t.Iterable[str]:
        return cardboard.name.lower(),

    @classmethod
    def extract_layout(cls, cardboard: Cardboard) -> t.Iterable[Layout]:
        return cardboard.layout,

    @classmethod
    def extract_cmc(cls, cardboard: Cardboard) -> t.Iterable[int]:
        return (card.cmc for card in cardboard.cards)

    @classmethod
    def extract_rarity(cls, cardboard: Cardboard) -> t.Iterable[Rarity]:
        return (printing.rarity for printing in cardboard.printings)

    @classmethod
    def extract_flags(cls, cardboard: Cardboard) -> t.Iterable[Flags]:
        return (printing.flags for printing in cardboard.printings)

    @classmethod
    def extract_type_line(cls, cardboard: Cardboard) -> t.Iterable[TypeLine]:
        return (card.type_line for card in cardboard.cards)

    @classmethod
    def extract_mana_cost(cls, cardboard: Cardboard) -> t.Iterable[ManaCost]:
        return (card.mana_cost for card in cardboard.cards)

    @classmethod
    def extract_color(cls, cardboard: Cardboard) -> t.Iterable[t.AbstractSet[Color]]:
        return (card.color for card in cardboard.cards)

    @classmethod
    def extract_colors(cls, cardboard: Cardboard) -> t.Iterable[t.AbstractSet[Color]]:
        return (card.color for card in cardboard.cards)

    @classmethod
    def extract_oracle(cls, cardboard: Cardboard) -> t.Iterable[str]:
        return (card.oracle_text.lower() for card in cardboard.cards)

    @classmethod
    def extract_flavor(cls, cardboard: Cardboard) -> t.Iterable[str]:
        return (face.flavor.lower() for printing in cardboard.printings for face in printing.faces)

    @classmethod
    def extract_power(cls, cardboard: Cardboard) -> t.Iterable[PTValue]:
        return (
            card.power_toughness.power
            for card in
            cardboard.cards
            if card.power_toughness is not None
        )

    @classmethod
    def extract_toughness(cls, cardboard: Cardboard) -> t.Iterable[PTValue]:
        return (
            card.power_toughness.toughness
            for card in
            cardboard.cards
            if card.power_toughness is not None
        )

    @classmethod
    def extract_loyalty(cls, cardboard: Cardboard) -> t.Iterable[PTValue]:
        return (card.loyalty for card in cardboard.cards)

    @classmethod
    def extract_artist(cls, cardboard: Cardboard) -> t.Iterable[str]:
        return (
            face.artist.name.lower()
            for printing in
            cardboard.printings
            for face in
            printing.faces
            if face.artist is None
        )

    @classmethod
    def extract_expansion(cls, cardboard: Cardboard) -> t.Iterable[Expansion]:
        return (printing.expansion for printing in cardboard.printings)

    @classmethod
    def extract_block(cls, cardboard: Cardboard) -> t.Iterable[Block]:
        return (
            printing.expansion.block
            for printing in
            cardboard.printings
            if printing.expansion is not None
        )


class PrintingStrategy(ExtractionStrategy[Printing]):

    @classmethod
    def extract_name(cls, printing: Printing) -> t.Iterable[str]:
        return printing.cardboard.name.lower(),

    @classmethod
    def extract_layout(cls, printing: Printing) -> t.Iterable[Layout]:
        return printing.cardboard.layout,

    @classmethod
    def extract_cmc(cls, printing: Printing) -> t.Iterable[int]:
        return (card.cmc for card in printing.cardboard.cards)

    @classmethod
    def extract_rarity(cls, printing: Printing) -> t.Iterable[Rarity]:
        return printing.rarity,

    @classmethod
    def extract_flags(cls, printing: Printing) -> t.Iterable[Flags]:
        return printing.flags,

    @classmethod
    def extract_type_line(cls, printing: Printing) -> t.Iterable[TypeLine]:
        return (card.type_line for card in printing.cardboard.cards)

    @classmethod
    def extract_mana_cost(cls, printing: Printing) -> t.Iterable[ManaCost]:
        return (
            card.mana_cost
            for card in
            printing.cardboard.cards
            if card.mana_cost is not None
        )

    @classmethod
    def extract_color(cls, printing: Printing) -> t.Iterable[t.AbstractSet[Color]]:
        return (card.color for card in printing.cardboard.cards)

    @classmethod
    def extract_colors(cls, printing: Printing) -> t.Iterable[t.AbstractSet[Color]]:
        return (card.color for card in printing.cardboard.cards)

    @classmethod
    def extract_oracle(cls, printing: Printing) -> t.Iterable[str]:
        return (card.oracle_text.lower() for card in printing.cardboard.cards)

    @classmethod
    def extract_flavor(cls, printing: Printing) -> t.Iterable[str]:
        return (face.flavor.lower() for face in printing.faces)

    @classmethod
    def extract_power(cls, printing: Printing) -> t.Iterable[PTValue]:
        return (
            card.power_toughness.power
            for card in
            printing.cardboard.cards
            if card.power_toughness is not None
        )

    @classmethod
    def extract_toughness(cls, printing: Printing) -> t.Iterable[PTValue]:
        return (
            card.power_toughness.toughness
            for card in
            printing.cardboard.cards
            if card.power_toughness is not None
        )

    @classmethod
    def extract_loyalty(cls, printing: Printing) -> t.Iterable[PTValue]:
        return (
            card.loyalty
            for card in
            printing.cardboard.cards
            if card.loyalty is not None
        )

    @classmethod
    def extract_artist(cls, printing: Printing) -> t.Iterable[str]:
        return (
            face.artist.name.lower()
            for face in
            printing.faces
            if face.artist is not None
        )

    @classmethod
    def extract_expansion(cls, printing: Printing) -> t.Iterable[Expansion]:
        return printing.expansion,

    @classmethod
    def extract_block(cls, printing: Printing) -> t.Iterable[Block]:
        return () if printing.expansion is None else (printing.expansion.block,)
