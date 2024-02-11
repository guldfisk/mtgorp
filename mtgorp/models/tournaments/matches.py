from __future__ import annotations

import typing as t
from abc import ABCMeta, abstractmethod

from hardcandy import fields
from hardcandy.schema import Schema
from yeetlong.errors import Errors

from mtgorp.models.tournaments.tournaments import CompletedMatch


class _MatchTypeMeta(ABCMeta):
    matches_map: t.MutableMapping[str, t.Type[MatchType]] = {}

    def __new__(mcs, classname, base_classes, attributes):
        klass = type.__new__(mcs, classname, base_classes, attributes)

        if "name" in attributes:
            mcs.matches_map[attributes["name"]] = klass

        return klass


class MatchType(object, metaclass=_MatchTypeMeta):
    name: str
    options_schema = Schema()
    allows_draws: bool = False

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def validate_result(self, result: CompletedMatch) -> Errors:
        pass

    def _serialize_args(self) -> t.Mapping[str, t.Any]:
        return {}

    def serialize(self) -> t.Mapping[str, t.Any]:
        return {
            "name": self.name,
            **self._serialize_args(),
        }

    @classmethod
    def deserialize(cls, values: t.Mapping[str, t.Any]) -> MatchType:
        return cls.matches_map[values["name"]](**{k: v for k, v in values.items() if k != "name"})


class MatchOfn(MatchType):
    options_schema = Schema({"n": fields.Integer(min=1, max=128, default=3)})

    def __init__(self, n: int, **kwargs):
        super().__init__(**kwargs)
        self._n = n

    @property
    def n(self) -> int:
        return self._n

    def __str__(self) -> str:
        return f"{self.name}{self._n}"

    def _serialize_args(self) -> t.Mapping[str, t.Any]:
        return {"n": self._n}

    @abstractmethod
    def validate_result(self, result: CompletedMatch) -> Errors:
        pass


class BestOfN(MatchOfn):
    name = "BON"
    allows_draws: bool = True

    def validate_result(self, result: CompletedMatch) -> Errors:
        errors = []
        if result.amount_completed_games != self._n:
            errors.append(
                "match has completed {} games, which does not match required {}.".format(
                    result.amount_completed_games,
                    self._n,
                )
            )
        return Errors(errors)


class FirstToN(MatchOfn):
    name = "FTN"
    options_schema = Schema({"n": fields.Integer(min=1, max=128, default=2)})

    def validate_result(self, result: CompletedMatch) -> Errors:
        errors = []
        max_wins = max(result.results.values())
        if max_wins != self._n:
            errors.append(
                "match not completed, leader has {} wins, which does not match required {}.".format(
                    max_wins,
                    self._n,
                )
            )
        if len(result.winners) > 1:
            errors.append("match cannot be a draw")
        return Errors(errors)
