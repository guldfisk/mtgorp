from __future__ import annotations

import typing as t

from abc import abstractmethod, ABCMeta

from mtgorp.models.tournaments.tournaments import CompletedMatch


class MatchValidationError(Exception):

    def __init__(self, error: str):
        super().__init__()
        self._error = error

    @property
    def error(self) -> str:
        return self._error

    def __repr__(self) -> str:
        return self._error


class _MatchTypeMeta(ABCMeta):
    matches_map: t.MutableMapping[str, t.Type[MatchType]] = {}

    def __new__(mcs, classname, base_classes, attributes):
        klass = type.__new__(mcs, classname, base_classes, attributes)

        if 'name' in attributes:
            mcs.matches_map[attributes['name']] = klass

        return klass


class MatchType(object, metaclass = _MatchTypeMeta):
    name: str

    @property
    def allows_draws(self) -> bool:
        return False

    @abstractmethod
    def validate_result(self, result: CompletedMatch) -> None:
        pass

    def _serialize_args(self) -> t.Mapping[str, t.Any]:
        return {}

    def serialize(self) -> t.Mapping[str, t.Any]:
        return {
            'name': self.name,
            **self._serialize_args,
        }

    @classmethod
    def deserialize(cls, values: t.Mapping[str, t.Any]) -> MatchType:
        return cls.matches_map[values['name']](**{k: v for k, v in values.items() if k != 'name'})


class MatchOfn(MatchType):

    def __init__(self, n: int):
        self._n = n

    @property
    def n(self) -> int:
        return self._n

    def __str__(self) -> str:
        return f'{self.name}{self._n}'

    def _serialize_args(self) -> t.Mapping[str, t.Any]:
        return {'n': self._n}


class BestOfN(MatchOfn):
    name = 'BON'

    @property
    def allows_draws(self) -> bool:
        return True

    def validate_result(self, result: CompletedMatch) -> None:
        if result.amount_completed_games != self._n:
            raise MatchValidationError(
                'match has completed {} games, which does not match required {}.'.format(
                    result.amount_completed_games,
                    self._n,
                )
            )


class FirstToN(MatchOfn):
    name = 'FTN'

    def validate_result(self, result: CompletedMatch) -> None:
        max_wins = max(result.results.keys())
        if max_wins != self._n:
            raise MatchValidationError(
                'match not completed, leader only has {} of {} required wins.'.format(
                    max_wins,
                    self._n,
                )
            )
        if len(result.winners) > 1:
            raise MatchValidationError('match cannot be a draw')
