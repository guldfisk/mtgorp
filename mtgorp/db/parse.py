import datetime
import logging
import re
import typing as t
from abc import abstractmethod

import ijson

from orp.database import OrpTable, O as _O, M as _M

from mtgorp.db.attributeparse import typeline, color, powertoughness, rarity, border, layout, boosterkey, loyalty, manacost, expansiontype
from mtgorp.db.attributeparse.exceptions import AttributeParseException
from mtgorp.db.database import DB
from mtgorp.db.exceptions import DbParseException
from mtgorp.db.limited.boosterinformation import BoosterInformation
from mtgorp.managejson import paths
from mtgorp.models import interfaces as i
from mtgorp.models.persistent.attributes.flags import Flag, Flags
from mtgorp.models.persistent.attributes.layout import Layout


parse_logger = logging.Logger('mtgorp.db.parse', logging.INFO)

M = t.TypeVar('M', bound = i.MtgModel)


class ModelParser(t.Generic[M]):

    def __init__(self, target: t.Type[M]):
        self._target = target

    @abstractmethod
    def parse(self, *args, **kwargs) -> M:
        pass


C = t.TypeVar('C', bound = i.Card)


class CardParser(ModelParser[C]):

    def __init__(self, target: t.Type[M]):
        super().__init__(target)
        self._seen_cards = set()

    @classmethod
    def _parse_colors(cls, cols):
        return {color.Parser.parse(s) for s in cols}

    def parse(self, raw_card) -> C:
        parse_logger.info(f'parsing Card {raw_card.get("faceName") or raw_card.get("name")}')

        try:
            name = raw_card.get('faceName') or raw_card['name']
        except KeyError:
            raise AttributeParseException('Cardboard has no name')

        if name in self._seen_cards:
            raise DbParseException('Duplicate card')

        self._seen_cards.add(name)

        power, toughness = raw_card.get('power', None), raw_card.get('toughness', None)

        pt = powertoughness.PowerToughness(
            powertoughness.Parser.parse_pt_value(power),
            powertoughness.Parser.parse_pt_value(toughness),
        ) if power is not None and toughness is not None else None

        try:
            mana_cost = manacost.Parser.parse(raw_card['manaCost'])
        except KeyError:
            mana_cost = None

        return self._target(
            name = name,
            type_line = typeline.Parser.parse(raw_card.get('type', '')),
            mana_cost = mana_cost,
            color = self._parse_colors(raw_card.get('colors', ())),
            oracle_text = re.sub('\(.*?\)', '', raw_card.get('text', ''), flags = re.IGNORECASE),
            power_toughness = pt,
            loyalty = (
                loyalty.Parser.parse(str(raw_card['loyalty']))
                if 'loyalty' in raw_card else
                None
            ),
            color_identity = self._parse_colors(raw_card.get('colorIdentity', ())),
        )


D = t.TypeVar('D', bound = i.Cardboard)


class CardboardParser(ModelParser[D]):

    @classmethod
    def get_cardboard_card_names(cls, raw_cardboard) -> t.Tuple[t.Sequence[str], t.Sequence[str]]:
        try:
            raw_card_layout = layout.Parser.parse(raw_cardboard[0]['layout'])

            if raw_card_layout in (
                Layout.STANDARD,
                Layout.SAGA,
                Layout.CLASS,
            ):
                return (
                    (raw_cardboard[0]['name'],),
                    (),
                )

            elif (
                raw_card_layout in
                (
                    Layout.SPLIT,
                    Layout.FLIP,
                    Layout.AFTERMATH,
                    Layout.ADVENTURE,
                )
            ):
                return (
                    tuple(
                        raw_card['faceName']
                        for raw_card in
                        sorted(
                            raw_cardboard,
                            key = lambda c: c['side']
                        )
                    ),
                    (),
                )

            elif raw_card_layout in (Layout.TRANSFORM, Layout.MODAL):
                return tuple(
                    (name,)
                    for name in
                    raw_cardboard[0]['name'].split(' // ')
                )

            elif raw_card_layout == Layout.MELD:
                if ' // ' in raw_cardboard[0]['name']:
                    return (
                        (raw_cardboard[0]['faceName'],),
                        (raw_cardboard[0]['name'].split(' // ')[1],),
                    )

            raise AttributeParseException('"{}" is not front side of layout'.format(raw_cardboard[0]['name']))

        except KeyError as e:
            raise AttributeParseException(f'Invalid cardboard names "{e}"')

    def parse(self, raw_cardboard, cards: OrpTable[str, D]) -> D:
        parse_logger.info(f'parsing Cardboard {raw_cardboard[0].get("name")}')

        try:
            front_names, back_names = self.get_cardboard_card_names(raw_cardboard)

            return self._target(
                front_cards = [cards[name] for name in front_names],
                back_cards = [cards[name] for name in back_names],
                layout = layout.Parser.parse(raw_cardboard[0]['layout']),
            )

        except KeyError:
            raise AttributeParseException('Cardboard has no layout')


A = t.TypeVar('A', bound = i.Artist)


class ArtistParser(ModelParser[A]):

    def parse(self, name: str, artists: OrpTable[str, A]) -> A:
        if not name:
            return None

        if name in artists:
            return artists[name]

        artist = self._target(name = name)
        artists.insert(artist)
        return artist


P = t.TypeVar('P', bound = i.Printing)
E = t.TypeVar('E', bound = i.Expansion)


class PrintingParser(ModelParser[P]):

    def __init__(self, target: t.Type[M], artist_parser: ArtistParser[A]):
        super().__init__(target)
        self._artist_parser = artist_parser

    @classmethod
    def _find_raw_printing_from_face_name(cls, face_name: str, raw_printings):
        for printing in raw_printings:
            if printing.get('faceName', '') == face_name:
                return printing
        raise AttributeParseException(f'No printing called "{face_name}"')

    def parse(
        self,
        raw_printing,
        raw_printings,
        expansion: E,
        artists: OrpTable[str, A],
        cardboards: OrpTable[str, D],
    ) -> P:
        parse_logger.info(f'parsing Printing {raw_printing.get("name")} [{expansion.code}] {raw_printing.get("identifiers", {}).get("multiverseId", "no multiverseId")}')

        try:
            name = raw_printing['name']

            cardboard: D = cardboards[name]

            if 'faceName' in raw_printing and raw_printing['faceName'] != cardboard.front_card.name:
                raise AttributeParseException('Printing not front')

            if cardboard.back_card is not None:
                raw_back_printing = self._find_raw_printing_from_face_name(cardboard.back_card.name, raw_printings)
                back_artist = self._artist_parser.parse(raw_back_printing.get('artist', None), artists)
                back_flavor = raw_back_printing.get('flavorText', None)
            else:
                back_artist = None
                back_flavor = None

            flags = []

            if raw_printing.get('timeshifted') or 'colorshifted' in raw_printing.get('frameEffects', ()):
                flags.append(Flag.TIMESHIFTED)

            information = BoosterInformation.information()
            if expansion.code in information:
                if 'flags' in information[expansion.code]:
                    for flag in information[expansion.code]['flags']:
                        if cardboard.name in flag.get('cards', ()):
                            try:
                                flags.append(Flag[flag.get('name', '')])
                            except KeyError:
                                pass

            collector_number = raw_printing.get(
                'number',
                raw_printing.get(
                    'mciNumber',
                ),
            )

            return self._target(
                id = int(raw_printing['identifiers']['multiverseId']),
                expansion = expansion,
                collector_number = (
                    -1
                    if collector_number is None else
                    int(
                        re.sub(
                            '[^\d]',
                            '',
                            collector_number,
                            flags = re.IGNORECASE,
                        )
                    )
                ),
                collector_string = collector_number or '',
                cardboard = cardboard,
                front_artist = self._artist_parser.parse(raw_printing.get('artist', None), artists),
                front_flavor = raw_printing.get('flavorText', None),
                back_artist = back_artist,
                back_flavor = back_flavor,
                rarity = rarity.Parser.parse(raw_printing['rarity']) if 'rarity' in raw_printing else None,
                in_booster = (
                    not raw_printing.get('isStarter')
                    or expansion.code in information
                    and 'blacklist' in information[expansion.code]
                    and cardboard.name in information[expansion.code]['blacklist']
                ),
                flags = Flags(flags),
            )

        except KeyError as e:
            raise AttributeParseException(f'Key error in printing parse: "{e}"')


B = t.TypeVar('B', bound = i.Block)


class BlockParser(ModelParser[B]):

    def parse(self, name: str, blocks: OrpTable[str, B]) -> B:
        if name in blocks:
            return blocks[name]

        block = self._target(name = name)
        blocks.insert(block)
        return block


class ExpansionParser(ModelParser[E]):
    _mythic_release_date = datetime.datetime(year = 2008, month = 8, day = 3)

    def __init__(
        self,
        target: t.Type[M],
        printing_parser: PrintingParser[P],
        block_parser: BlockParser[B],
    ):
        super().__init__(target)
        self._printing_parser = printing_parser
        self._block_parser = block_parser

        self._default_booster_key = boosterkey.Parser.parse(['rare'] + ['uncommon'] * 3 + ['common'] * 10 + ['land'])
        self._default_booster_key_with_mythic = boosterkey.Parser.parse(
            [['rare', 'mythic rare']]
            + ['uncommon'] * 3
            + ['common'] * 10
            + ['land']
        )

    def parse(
        self,
        raw_expansion,
        cardboards: OrpTable[str, D],
        printings: OrpTable[int, P],
        artists: OrpTable[str, A],
        blocks: OrpTable[str, B],
    ) -> E:
        parse_logger.info(f'parsing Expansion {raw_expansion.get("name")} [{raw_expansion.get("code").upper()}]')

        name = raw_expansion['name']
        code = raw_expansion['code'].upper()
        release_date = datetime.datetime.strptime(
            raw_expansion['releaseDate'], '%Y-%m-%d'
        ) if 'releaseDate' in raw_expansion else None

        information = BoosterInformation.information()

        expansion = self._target(
            name = name,
            code = code,
            block = self._block_parser.parse(raw_expansion['block'], blocks) if 'block' in raw_expansion else None,
            expansion_type = expansiontype.Parser.parse(raw_expansion.get('type')),
            release_date = release_date,
            booster_key = (
                boosterkey.Parser.parse(information[code]['booster_key'])
                if code in information and 'booster_key' in information[code] else
                (
                    boosterkey.Parser.parse(raw_expansion['boosterV3'])
                    if 'boosterV3' in raw_expansion else
                    (
                        self._default_booster_key_with_mythic
                        if release_date >= self._mythic_release_date else
                        self._default_booster_key
                    )
                )
            ),
            border = border.Parser.parse(raw_expansion['border']) if 'border' in raw_expansion else None,
            magic_card_info_code = raw_expansion.get('magicCardsInfoCode', None),
            mkm_name = raw_expansion.get('mkmName', None),
            mkm_id = raw_expansion.get('mkmId', None),
            fragment_dividers = (
                tuple(information[code].get('fragment_dividers', ()))
                if code in information else
                ()
            ),
        )

        for raw_printing in raw_expansion['cards']:
            try:
                printings.insert(
                    self._printing_parser.parse(
                        raw_printing = raw_printing,
                        raw_printings = raw_expansion['cards'],
                        expansion = expansion,
                        artists = artists,
                        cardboards = cardboards,
                    )
                )
            except DbParseException as e:
                parse_logger.info(f'failed to parse Printing {raw_printing.get("name")} [{code}] ({e})')

        return expansion

    @classmethod
    def post_parse(cls, expansions: OrpTable[str, E]):
        information = BoosterInformation.information()
        for expansion in expansions.values():
            if expansion.code in information and 'booster_expansion_collection' in information[expansion.code]:
                values = information[expansion.code]['booster_expansion_collection']
                expansion._booster_expansion_collection = i.ExpansionCollection(
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
                try:
                    basics = expansion if expansion.block is None else expansion.block.first_expansion
                except ValueError:
                    basics = expansion

                expansion._booster_expansion_collection = i.ExpansionCollection(
                    main = expansion,
                    basics = basics,
                )


class DatabaseCreator(t.Generic[DB]):
    _model_parser_map: t.Mapping[t.Type[i.MtgModel], t.Type[i.MtgModel]]

    def __init__(
        self,
        json_updated_at: datetime.datetime,
        *,
        all_cards_path: str = paths.ALL_CARDS_PATH,
        all_sets_path: str = paths.ALL_SETS_PATH,
        logging_path: str = paths.LOG_PATH,
    ):
        self._json_updated_at = json_updated_at
        self._all_cards_path = all_cards_path
        self._all_sets_path = all_sets_path
        self._logging_path = logging_path

    @abstractmethod
    def create_table_for_model(self, model: t.Type[i.MtgModel]) -> OrpTable:
        pass

    def create_card_table(self, raw_cards):
        cards_model = self._model_parser_map[i.Card]
        cards = self.create_table_for_model(cards_model)

        card_parser = CardParser(cards_model)

        for _, _cards in raw_cards:
            for card in _cards:
                try:
                    cards.insert(
                        card_parser.parse(card)
                    )
                except DbParseException as e:
                    parse_logger.info(f'failed to parse Card {card.get("name")} ({e})')

        return cards

    def create_cardboard_table(self, raw_cardboards, cards):
        cardboards_model = self._model_parser_map[i.Cardboard]
        cardboards = self.create_table_for_model(cardboards_model)

        cardboard_parser = CardboardParser(cardboards_model)

        for _, raw_cardboard in raw_cardboards:
            try:
                cardboards.insert(cardboard_parser.parse(raw_cardboard, cards))
            except DbParseException as e:
                parse_logger.info(f'failed to parse Cardboard {raw_cardboard[0].get("name")} ({e})')

        return cardboards

    def create_expansion_table(
        self,
        raw_expansions,
        cardboards: OrpTable[str, D],
        printings: OrpTable[int, P],
        artists: OrpTable[str, A],
        blocks: OrpTable[str, B],
    ):
        expansion_model = self._model_parser_map[i.Expansion]
        expansions = self.create_table_for_model(expansion_model)

        expansion_parser = ExpansionParser(
            expansion_model,
            PrintingParser(
                self._model_parser_map[i.Printing],
                ArtistParser(
                    self._model_parser_map[i.Artist],
                )
            ),
            BlockParser(
                self._model_parser_map[i.Block]
            ),
        )

        for code, expansion in raw_expansions:
            # TODO temp workaround duplicate multiverseIds in json
            if code.upper() in ['MB1', 'CMB1', 'CMB2', 'ONE', 'ONC', 'J22']:
                continue
            expansions.insert(
                expansion_parser.parse(
                    raw_expansion = expansion,
                    cardboards = cardboards,
                    printings = printings,
                    artists = artists,
                    blocks = blocks,
                )
            )
        expansion_parser.post_parse(expansions)
        return expansions

    @abstractmethod
    def _create_database_from_tables(self, tables: t.MutableMapping[str, OrpTable[_O, _M]]) -> DB:
        pass

    def _pre_run(self) -> None:
        pass

    def create_database(self) -> DB:
        self._pre_run()

        with open(
            self._all_cards_path, 'r', encoding = 'UTF-8'
        ) as all_cards_file, open(
            self._all_sets_path, 'r', encoding = 'UTF-8'
        ) as all_sets_file:
            handler = logging.FileHandler(self._logging_path, mode = 'w')
            parse_logger.addHandler(handler)

            try:
                raw_cards = ijson.kvitems(all_cards_file, 'data')

                cards = self.create_card_table(raw_cards)

                all_cards_file.seek(0)
                raw_cards = ijson.kvitems(all_cards_file, 'data')

                cardboards = self.create_cardboard_table(raw_cards, cards)

                artists = self.create_table_for_model(self._model_parser_map[i.Artist])
                blocks = self.create_table_for_model(self._model_parser_map[i.Block])
                printings = self.create_table_for_model(self._model_parser_map[i.Printing])

                raw_expansions = ijson.kvitems(all_sets_file, 'data')

                expansions = self.create_expansion_table(
                    raw_expansions = raw_expansions,
                    cardboards = cardboards,
                    printings = printings,
                    artists = artists,
                    blocks = blocks,
                )

                return self._create_database_from_tables(
                    {
                        'cards': cards,
                        'cardboards': cardboards,
                        'printings': printings,
                        'artists': artists,
                        'blocks': blocks,
                        'expansions': expansions,
                    }
                )

            finally:
                parse_logger.removeHandler(handler)
