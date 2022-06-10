from __future__ import annotations

from functools import total_ordering

from .LeitnerCardStats import LeitnerCardStats
from .LeitnerDeck import LeitnerDeck
from .LeitnerCardData import LeitnerCardData


@total_ordering
class LeitnerCard:

    def __init__(self):
        self.stats: LeitnerCardStats = LeitnerCardStats()
        self.deck: LeitnerDeck | None = None
        self.data: LeitnerCardData | None = None

    def __eq__(self, other) -> bool:
        return self.sort_key() == other.sort_key()

    def __lt__(self, other) -> bool:
        return self.sort_key() < other.sort_key()

    def get_my_next_session_threshold(self, max_shows: int) -> int:
        """
           How many times a card must be shown in the session.
           When using strict Pimsleur timings, the Pimsleur timing value based on
           maxShows must not exceed 1/2 to 3/4 the session length or else the card will
           never be successfully marked as answered correctly all times and moved to the
           next higher Leitner box! For example: A 5 minute session can not have a maxShows > 3.
           Basically returns the supplied value - the current Leitner box the card is in.
       """
        leitner_box: int = self.stats.leitner_box
        return max(max_shows - leitner_box, 1)

    def id(self) -> str:
        return self.data.id() if self.data else None

    def reset_stats(self) -> None:
        self.stats.correct = True
        self.stats.shown_count = 0
        self.stats.total_shown_time = 0.0

    def reset_tries_remaining(self, max_tries_remaining: int = 3) -> None:
        self.stats.tries_remaining = self.get_my_next_session_threshold(max_tries_remaining)

    def sort_key(self) -> str:
        return self.data.sort_key() if self.data else None
