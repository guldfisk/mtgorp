from abc import ABC, abstractmethod

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


class MatchType(ABC):

    @abstractmethod
    def validate_result(self, result: CompletedMatch) -> None:
        pass


class BestOfN(MatchType):

    def __init__(self, n: int):
        self._n = n

    @property
    def n(self) -> int:
        return self._n

    def validate_result(self, result: CompletedMatch) -> None:
        if result.amount_completed_games != self._n:
            raise MatchValidationError(
                'match has completed {} games, which does not match required {}.'.format(
                    result.amount_completed_games,
                    self._n,
                )
            )


class FirstToN(MatchType):

    def __init__(self, n: int):
        self._n = n

    @property
    def n(self) -> int:
        return self._n

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
