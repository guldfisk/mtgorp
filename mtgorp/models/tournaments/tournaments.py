import itertools
import math
import random
import typing as t

from abc import ABC, abstractmethod
from collections import defaultdict

from frozendict import frozendict


class Player(object):

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __hash__(self) -> int:
        return hash(self._name)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._name == other._name
        )

    def __repr__(self) -> str:
        return self._name


class ScheduledMatch(object):

    def __init__(self, players: t.FrozenSet[Player]):
        self._players = players

    @property
    def players(self) -> t.AbstractSet[Player]:
        return self._players

    def __hash__(self) -> int:
        return hash(self._players)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._players == other._players
        )

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(map(str, self._players)),
        )


class CompletedMatch(object):

    def __init__(self, results: t.Mapping[Player, int], draws: int = 0):
        self._results = frozendict(results)
        self._draws = draws

    @property
    def results(self) -> t.Mapping[Player, int]:
        return self._results

    @property
    def draws(self) -> int:
        return self._draws

    @property
    def amount_completed_games(self) -> int:
        return sum(self.results.values()) + self.draws

    @property
    def winners(self) -> t.FrozenSet[Player]:
        _max_wins = max(self._results.values())
        return frozenset(
            player
            for player, wins in
            self._results.items()
            if wins == _max_wins
        )

    @property
    def winner(self) -> Player:
        winners = self.winners
        if len(winners) > 1:
            raise RuntimeError('draw')
        return winners.__iter__().__next__()

    def __hash__(self) -> int:
        return hash(self._results)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._results == other._results
        )

    def __repr__(self) -> str:
        return '{}({}, {})'.format(
            self.__class__.__name__,
            ', '.join('{}: {}'.format(player, wins) for player, wins in self._results.items()),
            self._draws,
        )


class Round(object):

    def __init__(self, matches: t.FrozenSet[ScheduledMatch]):
        self._matches = matches

    @property
    def matches(self) -> t.AbstractSet[ScheduledMatch]:
        return self._matches

    def __hash__(self) -> int:
        return hash(self._matches)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._matches == other._matches
        )

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(map(str, self._matches)),
        )


class CompletedRound(object):

    def __init__(self, results: t.FrozenSet[CompletedMatch]):
        self._results = results

    @property
    def results(self) -> t.AbstractSet[CompletedMatch]:
        return self._results

    def __hash__(self) -> int:
        return hash(self._results)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._results == other._results
        )

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(map(str, self._results)),
        )


class TournamentResult(object):

    def __init__(self, winners: t.FrozenSet[Player]):
        self._winners = winners

    @property
    def winners(self) -> t.FrozenSet[Player]:
        return self._winners

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(map(str, self._winners)),
        )


class ResultException(Exception):
    pass


class Tournament(ABC):
    name: str
    _players: t.FrozenSet[Player]

    @property
    @abstractmethod
    def allow_match_draws(self) -> bool:
        pass

    @property
    @abstractmethod
    def round_amount(self) -> int:
        pass

    @abstractmethod
    def get_round(self, previous_rounds: t.Sequence[CompletedRound] = ()) -> t.Optional[Round]:
        pass

    @abstractmethod
    def get_result(self, previous_rounds: t.Sequence[CompletedRound]) -> TournamentResult:
        pass


class AllMatches(Tournament):
    name = 'all_matches'

    def __init__(self, players: t.FrozenSet[Player]):
        self._players = players

    @property
    def allow_match_draws(self) -> bool:
        return True

    @property
    def round_amount(self) -> int:
        return 1

    def get_round(self, previous_rounds: t.Sequence[CompletedRound] = ()) -> t.Optional[Round]:
        if previous_rounds:
            return None
        return Round(
            frozenset(
                ScheduledMatch(
                    frozenset(players)
                ) for players in
                itertools.combinations(self._players, 2)
            )
        )

    def get_result(self, previous_rounds: t.Sequence[CompletedRound]) -> TournamentResult:
        try:
            _round = previous_rounds.__iter__().__next__()
        except StopIteration:
            raise ResultException('tournament not complete')

        player_wins_map = defaultdict(int)

        for result in _round.results:
            winners = result.winners
            if len(winners) == 1:
                player_wins_map[winners.__iter__().__next__()] += 1

        max_wins = max(player_wins_map.values())

        winner_candidates = [
            player
            for player, wins in
            player_wins_map.items()
            if wins == max_wins
        ]

        if len(winner_candidates) == 1:
            return TournamentResult(frozenset(winner_candidates))

        player_game_wins_map = defaultdict(int)

        for result in _round.results:
            for player, wins in result.results.items():
                if player in winner_candidates:
                    player_game_wins_map[player] += wins

        max_game_wins = max(player_game_wins_map.values())

        return TournamentResult(
            frozenset(
                player
                for player, wins in
                player_game_wins_map.items()
                if wins == max_game_wins
            )
        )


class Swiss(Tournament):
    name = 'swiss'

    def __init__(self, players: t.FrozenSet[Player], rounds: int):
        self._players = players
        self._rounds = rounds

    @property
    def allow_match_draws(self) -> bool:
        return True

    @property
    def round_amount(self) -> int:
        return self._rounds

    @classmethod
    def _get_maps(
        cls,
        rounds: t.Sequence[CompletedRound] = (),
    ) -> t.Tuple[t.Mapping[Player, int], t.Mapping[Player, int], t.Mapping[Player, int]]:
        match_wins_map = defaultdict(int)
        game_wins_map = defaultdict(int)
        buys_map = defaultdict(int)

        for _round in rounds:
            for result in _round.results:
                if len(result.results) == 1:
                    buys_map[result.results.__iter__().__next__()] += 1
                else:
                    for player, wins in result.results.items():
                        game_wins_map[player] += wins
                winners = result.winners
                if len(winners) == 1:
                    match_wins_map[winners.__iter__().__next__()] += 1

        return match_wins_map, game_wins_map, buys_map

    def get_round(self, previous_rounds: t.Sequence[CompletedRound] = ()) -> t.Optional[Round]:
        if len(previous_rounds) >= self._rounds:
            return None

        match_wins_map, game_wins_map, buys_map = self._get_maps(previous_rounds)

        players = list(self._players)

        random.shuffle(players)

        ranked_players = sorted(
            players,
            key = lambda p: (match_wins_map[p], game_wins_map[p], -buys_map[p]),
        )

        matches = []

        if len(ranked_players) & 1:
            min_buys = min(buys_map[player] for player in self._players)
            for idx, player in enumerate(ranked_players):
                if buys_map[player] == min_buys:
                    matches.append(
                        ScheduledMatch(
                            frozenset(
                                (
                                    ranked_players.pop(idx),
                                )
                            )
                        )
                    )
                    break

        for idx in range(0, len(ranked_players), 2):
            matches.append(
                ScheduledMatch(
                    frozenset(ranked_players[idx:idx + 2])
                )
            )

        return Round(
            frozenset(matches)
        )

    def get_result(self, previous_rounds: t.Sequence[CompletedRound]) -> TournamentResult:
        if len(previous_rounds) < self._rounds:
            raise ResultException('tournament not complete')

        match_wins_map, game_wins_map, buys_map = self._get_maps(previous_rounds)
        results_map = defaultdict(list)

        for player in self._players:
            results_map[(match_wins_map[player], game_wins_map[player], -buys_map[player])].append(player)

        return TournamentResult(
            frozenset(
                results_map[max(results_map.keys())]
            )
        )


class SingleElimination(Tournament):
    name = 'single_elimination'

    def __init__(self, players: t.FrozenSet[Player]):
        self._players = players

    @property
    def allow_match_draws(self) -> bool:
        return False

    @property
    def round_amount(self) -> int:
        return int(math.ceil(math.log(len(self._players), 2)))

    def get_round(self, previous_rounds: t.Sequence[CompletedRound] = ()) -> t.Optional[Round]:
        if previous_rounds and len(previous_rounds[-1].results) <= 1:
            return None

        buys_map = defaultdict(int)

        for _round in previous_rounds:
            for result in _round.results:
                if len(result.results) == 1:
                    buys_map[result.results.__iter__().__next__()] += 1

        players = [result.winner for result in previous_rounds[-1].results] if previous_rounds else list(self._players)

        random.shuffle(players)

        matches = []

        if len(players) & 1:
            min_buys = min(buys_map[player] for player in self._players)
            for idx, player in enumerate(players):
                if buys_map[player] == min_buys:
                    matches.append(
                        ScheduledMatch(
                            frozenset(
                                (
                                    players.pop(idx),
                                )
                            )
                        )
                    )
                    break

        for idx in range(0, len(players), 2):
            matches.append(
                ScheduledMatch(
                    frozenset(players[idx:idx + 2])
                )
            )

        return Round(
            frozenset(matches)
        )

    def get_result(self, previous_rounds: t.Sequence[CompletedRound]) -> TournamentResult:
        if not previous_rounds or not len(previous_rounds[-1].results) == 1:
            raise ResultException('tournament not complete')

        return TournamentResult(
            frozenset(
                (
                    previous_rounds[-1].results.__iter__().__next__().winner,
                )
            )
        )

# class DoubleElimination(Tournament):
#     name = 'double_elimination'
#
#     def __init__(self, players: t.FrozenSet[Player]):
#         self._players = players
#
#     def get_round(self, previous_rounds: t.Sequence[CompletedRound] = ()) -> t.Optional[Round]:
#         pass
#
#     def get_result(self, previous_rounds: t.Sequence[CompletedRound]) -> TournamentResult:
#         pass
