import json
import datetime
import os
import sys
import re
import typing as t

from orp.database import Table
from orp.persist import PicklePersistor

from mtgorp.managejson import paths, update
from mtgorp.db.database import CardDatabase
from mtgorp.db.attributeparse import (
    typeline, color, powertoughness, rarity, border, layout, boosterkey, loyalty, manacost
)
from mtgorp.db.attributeparse.exceptions import AttributeParseException
from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes.flags import Flag, Flags
from mtgorp.models.persistent.card import Card
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.printing import Printing
from mtgorp.models.persistent.artist import Artist
from mtgorp.models.persistent.block import Block
from mtgorp.models.persistent.expansion import Expansion
from mtgorp.db.limited.boosterinformation import BoosterInformation
from mtgorp.models.limited.boostergen import ExpansionCollection


class _CardParser(object):

    @classmethod
    def _parse_colors(cls, cols):
        return {color.Parser.parse(s) for s in cols}

    @classmethod
    def parse(cls, raw_card):
        try:
            name = raw_card['name']
        except KeyError:
            raise AttributeParseException("Cardboard has no name")

        power, toughness = raw_card.get('power', None), raw_card.get('toughness', None)

        pt = powertoughness.PowerToughness(
            powertoughness.Parser.parse_pt_value(power),
            powertoughness.Parser.parse_pt_value(toughness),
        ) if power is not None and toughness is not None else None

        try:
            mana_cost = manacost.Parser.parse(raw_card['manaCost'])
        except KeyError:
            mana_cost = None

        return Card(
            name = name,
            type_line = typeline.Parser.parse(raw_card.get('type', '')),
            mana_cost = mana_cost,
            color = cls._parse_colors(raw_card.get('colors', ())),
            oracle_text = re.sub('\(.*?\)', '', raw_card.get('text', ''), flags = re.IGNORECASE),
            power_toughness = pt,
            loyalty = (
                loyalty.Parser.parse(str(raw_card['loyalty']))
                if 'loyalty' in raw_card else
                None
            ),
            color_identity = cls._parse_colors(raw_card.get('colorIdentity', ())),
        )


class _CardboardParser(object):

    @classmethod
    def get_cardboard_card_names(cls, raw_card):
        try:
            name = raw_card['name']
            raw_card_layout = layout.Parser.parse(raw_card['layout'])

            if raw_card_layout == Layout.STANDARD or raw_card_layout == Layout.SAGA:
                return (
                    (name,),
                    (),
                )

            elif (
                raw_card_layout == Layout.SPLIT
                or raw_card_layout == Layout.FLIP
                or raw_card_layout == Layout.AFTERMATH
                or raw_card_layout == Layout.ADVENTURE
            ):
                if name == raw_card['names'][0]:
                    return (
                        tuple(raw_card['names']),
                        (),
                    )

            elif raw_card_layout == Layout.TRANSFORM:
                if name == raw_card['names'][0]:
                    return (
                        (name,),
                        (raw_card['names'][1],),
                    )

            elif raw_card_layout == Layout.MELD:
                if name in (raw_card['names'][0], raw_card['names'][-1]):
                    return (
                        (name,),
                        (raw_card['names'][1],),
                    )

            raise AttributeParseException(f'"{name}" is not front side of layout')

        except KeyError as e:
            raise AttributeParseException(f'Invalid cardboard names "{e}"')

    @classmethod
    def parse(cls, raw_card, cards: Table):
        try:
            front_names, back_names = cls.get_cardboard_card_names(raw_card)

            return Cardboard(
                front_cards = tuple(cards[name] for name in front_names),
                back_cards = tuple(cards[name] for name in back_names),
                layout = layout.Parser.parse(raw_card['layout']),
            )

        except KeyError:
            raise AttributeParseException('Cardboard has no layout')


class _ArtistParser(object):

    @classmethod
    def parse(cls, name: str, artists: Table):
        if not name:
            return None

        artist = Artist(name)

        if not artist.name in artists:
            artists.insert(artist)
            return artist

        return artists[name]


class _PrintingParser(object):

    @classmethod
    def _find_raw_printing_from_name(cls, name: str, raw_printings):
        for printing in raw_printings:
            if printing.get('name', '') == name:
                return printing
        raise AttributeParseException(f'No printing called "{name}"')

    @classmethod
    def parse(cls, raw_printing, raw_printings, expansion: Expansion, artists: Table, cardboards: Table):
        try:
            name = raw_printing['name']

            front_names, back_names = _CardboardParser.get_cardboard_card_names(raw_printing)
            cardboard = cardboards[
                Cardboard.calc_name(front_names + back_names)
            ]

            if name != cardboard.front_card.name:
                raise AttributeParseException('Printing not front')

            if cardboard.back_card is not None:
                raw_back_printing = cls._find_raw_printing_from_name(cardboard.back_card.name, raw_printings)
                back_artist = _ArtistParser.parse(raw_back_printing.get('artist', None), artists)
                back_flavor = raw_back_printing.get('flavorText', None)
            else:
                back_artist = None
                back_flavor = None

            flags = []

            if raw_printing.get('timeshifted'):
                flags.append(Flag.TIMESHIFTED)

            information = BoosterInformation.information()
            if expansion.code in information:
                if 'blacklist' in information[expansion.code]:
                    in_booster = not cardboard.name in information[expansion.code]['blacklist']
                else:
                    in_booster = True
                if 'flags' in information[expansion.code]:
                    for flag in information[expansion.code]['flags']:
                        if cardboard.name in flag.get('cards', ()):
                            try:
                                flags.append(Flag[flag.get('name', '')])
                            except KeyError:
                                pass
            else:
                in_booster = True

            collector_number = raw_printing.get(
                'number',
                raw_printing.get(
                    'mciNumber',
                ),
            )

            return Printing(
                id = raw_printing['multiverseId'],
                expansion = expansion,
                collector_number = (
                    -1
                    if collector_number is None else
                    int(
                        re.sub(
                            '[^\d]',
                            '',
                            collector_number,
                            flags = re.IGNORECASE
                        )
                    )
                ),
                cardboard = cardboard,
                front_artist = _ArtistParser.parse(raw_printing.get('artist', None), artists),
                front_flavor = raw_printing.get('flavorText', None),
                back_artist = back_artist,
                back_flavor = back_flavor,
                rarity = rarity.Parser.parse(raw_printing['rarity']) if 'rarity' in raw_printing else None,
                in_booster = in_booster,
                flags = Flags(flags),
            )

        except KeyError as e:
            raise AttributeParseException(f'Key error in printing parse: "{e}"')


class _BlockParser(object):

    @classmethod
    def parse(cls, name: str, blocks: Table):
        block = Block(name = name)

        if not block.name in blocks:
            blocks.insert(block)
            return block

        return blocks[name]


class _ExpansionParser(object):

    @classmethod
    def parse(cls, raw_expansion, cardboards: Table, printings: Table, artists: Table, blocks: Table):
        try:
            name = raw_expansion['name']
            code = raw_expansion['code'].upper()
            if code == 'NMS':
                code = 'NEM'
            release_date = datetime.datetime.strptime(
                raw_expansion['releaseDate'], '%Y-%m-%d'
            ).date() if 'releaseDate' in raw_expansion else None

            information = BoosterInformation.information()
            expansion = Expansion(
                name = name,
                code = code,
                block = _BlockParser.parse(raw_expansion['block'], blocks) if 'block' in raw_expansion else None,
                release_date = release_date,
                booster_key = (
                    boosterkey.Parser.parse(information[code]['booster_key'])
                    if code in information and 'booster_key' in information[code] else
                    boosterkey.Parser.parse(tuple(raw_expansion.get('booster', ())))
                ),
                border = border.Parser.parse(raw_expansion['border']) if 'border' in raw_expansion else None,
                magic_card_info_code = raw_expansion.get('magicCardsInfoCode', None),
                mkm_name = raw_expansion.get('mkm_name', None),
                mkm_id = raw_expansion.get('mkm_id', None),
                fragment_dividers = (
                    tuple(information[code].get('fragment_dividers', ()))
                    if code in information else
                    ()
                ),
            )

            for raw_printing in raw_expansion['cards']:
                try:
                    printings.insert(
                        _PrintingParser.parse(
                            raw_printing = raw_printing,
                            raw_printings = raw_expansion['cards'],
                            expansion = expansion,
                            artists = artists,
                            cardboards = cardboards,
                        )
                    )
                except AttributeParseException:
                    pass

            return expansion

        except KeyError:
            raise AttributeParseException('Key error in expansion parse: "{e}"')

    @classmethod
    def post_parse(cls, expansions: t.Dict[str, Expansion]):
        information = BoosterInformation.information()
        for expansion in expansions.values():
            # todo find out how promo subsets was renamed and adjust limited data json
            # if expansion.code in information and 'booster_expansion_collection' in information[expansion.code]:
            if False:
                values = information[expansion.code]['booster_expansion_collection']
                expansion._booster_expansion_collection = ExpansionCollection(
                    main = expansion,
                    **{
                        key:
                            (
                                expansions[values[key][0]]
                                if values[key][1] is None
                                else expansions[values[key][0]].fragments[values[key][1]]
                            )
                        for key in
                        values
                    },
                )
            else:
                expansion._booster_expansion_collection = ExpansionCollection(
                    main = expansion,
                    basics = expansion if expansion.block is None else expansion.block.expansions_chronologically[0],
                )


class DatabaseCreator(object):

    @classmethod
    def create_card_table(cls, raw_cards):
        cards = Table()
        for name in raw_cards:
            try:
                cards.insert(
                    _CardParser.parse(raw_cards[name])
                )
            except AttributeParseException:
                pass
        return cards

    @classmethod
    def create_cardboard_table(cls, raw_cards, cards):
        cardboards = Table()
        for name in raw_cards:
            try:
                cardboards.insert(
                    _CardboardParser.parse(raw_cards[name], cards)
                )
            except AttributeParseException:
                pass
        return cardboards

    @classmethod
    def create_expansion_table(
        cls,
        raw_expansions,
        cardboards: Table,
        printings: Table,
        artists: Table,
        blocks: Table
    ):
        expansions = Table()
        for code in raw_expansions:
            try:
                expansions.insert(
                    _ExpansionParser.parse(
                        raw_expansion = raw_expansions[code],
                        cardboards = cardboards,
                        printings = printings,
                        artists = artists,
                        blocks = blocks,
                    )
                )
            except AttributeParseException:
                pass
        _ExpansionParser.post_parse(expansions)
        return expansions

    @classmethod
    def create_database(
        cls,
        all_cards_path = paths.ALL_CARDS_PATH,
        all_sets_path = paths.ALL_SETS_PATH,
    ):
        with open(all_cards_path, 'r', encoding = 'UTF-8') as f:
            raw_cards = json.load(f)
        with open(all_sets_path, 'r', encoding = 'UTF-8') as f:
            raw_expansions = json.load(f)

        cards = cls.create_card_table(raw_cards)
        cardboards = cls.create_cardboard_table(raw_cards, cards)
        artists = Table()
        blocks = Table()
        printings = Table()
        expansions = cls.create_expansion_table(
            raw_expansions = raw_expansions,
            cardboards = cardboards,
            printings = printings,
            artists = artists,
            blocks = blocks,
        )

        return CardDatabase(
            cards = cards,
            cardboards = Table(
                {
                    pk: cardboard
                    for pk, cardboard in
                    cardboards.items()
                    if cardboard.printings
                }
            ),
            printings = printings,
            artists = artists,
            blocks = blocks,
            expansions = expansions,
        )


def update_database(
    all_cards_path = paths.ALL_CARDS_PATH,
    all_sets_path = paths.ALL_SETS_PATH,
    db_path = paths.APP_DATA_PATH,
) -> CardDatabase:
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    if not os.path.exists(paths.ALL_CARDS_PATH) or not os.path.exists(paths.ALL_SETS_PATH):
        update.check_and_update()

    previous_recursion_limit = sys.getrecursionlimit()

    db = DatabaseCreator.create_database(
        all_cards_path,
        all_sets_path,
    )

    try:
        sys.setrecursionlimit(50000)
        PicklePersistor(os.path.join(paths.APP_DATA_PATH, 'db')).save(db)
    finally:
        sys.setrecursionlimit(previous_recursion_limit)

    return db


if __name__ == '__main__':
    update_database()
