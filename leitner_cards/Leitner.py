import math
from abc import abstractmethod
from collections.abc import MutableSequence
from enum import Enum
from functools import total_ordering
from typing import Iterable
from typing import overload


class LeitnerSkillLevel(Enum):
    def __init__(self, english: str, level: int):
        pass

    NEWBIE = ("Newbie", 0)
    NOVICE = ("Novice", 1)
    ROOKIE = ("Rookie", 2)
    BEGINNER = ("Beginner", 3)
    APPRENTICE = ("Apprentice", 4)
    INTERMEDIATE = ("Intermediate", 5)
    ADVANCED = ("Advanced", 6)
    PROFICIENT = ("Proficient", 7)
    EXPERT = ("Expert", 8)
    MASTER = ("Master", 9)
    GRANDMASTER = ("Grandmaster", 10)

    @classmethod
    def for_level(cls, level_number: int):
        level: LeitnerSkillLevel = cls.NEWBIE
        for maybe in cls:
            if maybe.get_level() == level_number:
                return maybe
            if level.get_level() < maybe.get_level() < level_number:
                level = maybe
        return level

    @classmethod
    def get_next(cls, level):
        if not level:
            return LeitnerSkillLevel.Newbie
        return level.next()

    def get_achievement_points(self) -> int:
        return self.value[1] * 5

    def get_english(self) -> str:
        return self.value[0]

    def get_level(self) -> int:
        return self.value[1]

    def next(self):
        return LeitnerSkillLevel.for_level(self.get_level() + 1)

    def __str__(self) -> str:
        return self.get_english()


class LeitnerCardStats:

    def __init__(self):

        self.correct: bool = False
        self.leitner_box: int = 0
        self.pimsleur_box: int = 0
        self.show_again_delay: float = 0.0
        self.shown_count: int = 0
        self.total_shown_time: float = 0.0
        self.tries_remaining: int = 0
        self.new_card: bool = False
        self.next_session_show: int = 0

    def leitner_box_dec(self) -> None:
        if self.leitner_box > 0:
            self.leitner_box -= 1

    def leitner_box_inc(self) -> None:
        self.leitner_box += 1

    def pimsleur_box_dec(self) -> None:
        if self.pimsleur_box > 0:
            self.pimsleur_box -= 1

    def pimsleur_box_inc(self) -> None:
        self.pimsleur_box += 1

    def tries_remaining_dec(self) -> None:
        if self.tries_remaining > 0:
            self.tries_remaining -= 1

    def tries_remaining_inc(self) -> None:
        self.tries_remaining += 1

    def has_tries_remaining(self) -> bool:
        return self.tries_remaining > 0


@total_ordering
class LeitnerCardData:
    def __init__(self):
        pass

    def __eq__(self, other) -> bool:
        return self.sort_key() == other.sort_key()

    def __lt__(self, other) -> bool:
        return self.sort_key() < other.sort_key()

    @abstractmethod
    def id(self) -> str: ...

    @abstractmethod
    def sort_key(self) -> str: ...


@total_ordering
class LeitnerCard:

    def __init__(self):
        self.stats: LeitnerCardStats = LeitnerCardStats()
        self.deck: LeitnerDeck = None
        self.data: LeitnerCardData = None

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


class LeitnerDeck(MutableSequence[LeitnerCard]):

    def __set_deck(self, value: LeitnerCard) -> None:
        if value:
            if value.deck:
                value.deck.remove(value)
            value.deck = self

    def insert(self, index: int, value: LeitnerCard) -> None:
        self.__set_deck(value)
        self.__list.insert(index, value)

    @overload
    @abstractmethod
    def __getitem__(self, i: int) -> LeitnerCard:
        ...

    @overload
    @abstractmethod
    def __getitem__(self, s: slice) -> MutableSequence[LeitnerCard]:
        ...

    def __getitem__(self, i: int) -> LeitnerCard:
        return self.__list.__getitem__(i)

    @overload
    @abstractmethod
    def __setitem__(self, i: int, o: LeitnerCard) -> None:
        ...

    @overload
    @abstractmethod
    def __setitem__(self, s: slice, o: Iterable[LeitnerCard]) -> None:
        ...

    def __setitem__(self, i: int, o: LeitnerCard) -> None:
        self.__set_deck(o)
        self.__list.__setitem__(i, o)

    @overload
    @abstractmethod
    def __delitem__(self, i: int) -> None:
        ...

    @overload
    @abstractmethod
    def __delitem__(self, i: slice) -> None:
        ...

    def __delitem__(self, i: int) -> None:
        item = self.__getitem__(i)
        if item:
            item.deck = None
        self.__list.__delitem__(i)

    def __len__(self) -> int:
        return self.__list.__len__()

    def __init__(self):
        super(LeitnerDeck, self).__init__()
        self.__list: list[LeitnerCard] = list()


class LeitnerDeckStats:
    FULLY_LEARNED_BOX: int = 10
    JUST_LEARNED_BOX: int = 1
    PROFICIENT_BOX: int = 5

    def __init__(self, deck: LeitnerDeck = None):
        self.active_cards: int = 0
        self.total_cards: int = 0
        self.full_score: int = 0
        self.last_run: float = 0
        self.next_run: float = 0
        self.last_score: int = 0
        self.skill_level: LeitnerSkillLevel = LeitnerSkillLevel.NEWBIE
        self.long_term: int = 0
        self.medium_term: int = 0
        self.perfect: bool = False
        self.proficiency: int = 0
        self.session_score: int = 0
        self.short_term: int = 0
        self.signature: str = ""
        self.version: int = 0

        if not deck:
            return

        """
            Set "level" to ceil(average box value) found in active deck. Negative box
            values are ignored.
        """

        box_sum: int = 0
        for card in deck:
            stats: LeitnerCardStats = card.stats
            box_sum += stats.leitner_box if stats.leitner_box > 0 else 0
        self.skill_level = LeitnerSkillLevel.for_level(int(math.ceil(box_sum / float(len(deck)))))

        """
            Set "fullScore" to sum of all box values found in active deck
        """

        box_sum = 0
        for card in deck:
            box_sum += card.stats.leitner_box
        self.full_score = box_sum

        """
             Set last score based on timings of most recent session. Cards with errors 
             count as "-1" each. Apply "boxlevel" values as bonus points.
        """

        MAX_CARD_SCORE: float = 60
        score: float = 0
        perfect: bool = True
        for card in deck:
            stats = card.stats
            if stats.shown_count == 0:
                continue
            if not stats.correct:
                score -= MAX_CARD_SCORE
                perfect = False
            avg_show_time: float = stats.total_shown_time / stats.shown_count
            card_score: float = MAX_CARD_SCORE - avg_show_time
            if card_score < 1:
                card_score = 1
            score += card_score + stats.leitner_box
        if perfect:
            score *= 1.1
        self.last_score = math.ceil(score)
        self.perfect = perfect

        """
            Calculate total proficiency with active cards (based on most recent noErrors flag)
        """

        total_cards: int = len(deck)
        correct_count: int = 0
        for card in deck:
            if card.stats.correct:
                correct_count += 1
        self.proficiency = int(100 * correct_count / total_cards)

        """
            How many are "fully learned" out of the active deck?
        """

        self.long_term = 0
        for card in deck:
            if card.stats.leitner_box >= LeitnerDeckStats.FULLY_LEARNED_BOX:
                self.long_term += 1

        """
            count all active cards that aren't "fully learned"
        """
        self.active_cards = len(deck) - self.long_term

        """
            How many are "well known" out of the active deck? (excluding full learned ones)
        """
        self.medium_term = 0
        for card in deck:
            leitner_box = card.stats.leitner_box
            if LeitnerDeckStats.PROFICIENT_BOX <= leitner_box < LeitnerDeckStats.FULLY_LEARNED_BOX:
                self.medium_term += 1

        """
            How many are "short term known" out of the active deck? (excluding full learned ones)
        """

        self.short_term = 0
        for card in deck:
            leitner_box = card.stats.leitner_box
            if LeitnerDeckStats.JUST_LEARNED_BOX <= leitner_box < LeitnerDeckStats.PROFICIENT_BOX:
                self.short_term += 1


class LeitnerCardUtils:

    def __init__(self):
        pass

    pimsleur_intervals_sec: list = None
    sm2_intervals_sec: list = None
    sm2_intervals_days: list = None

    @classmethod
    def get_next_interval(cls, correct_in_a_row: int) -> float:
        """
        Pimsleur staggered intervals (powers of 5) seconds
        :param correct_in_a_row:
        :return:
        """
        if correct_in_a_row < 0:
            return cls.pimsleur_intervals_sec[0]
        if correct_in_a_row >= len(cls.pimsleur_intervals_sec):
            return cls.pimsleur_intervals_sec[-1]
        return cls.pimsleur_intervals_sec[correct_in_a_row]

    @classmethod
    def get_next_session_interval_secs(cls, box: int) -> float:
        """
        SM2 staggered intervals (powers of 1.7) days as seconds
        :param box:
        :return:
        """
        if box < 0:
            return cls.sm2_intervals_sec[0]
        if box >= len(cls.sm2_intervals_sec):
            return cls.sm2_intervals_sec[-1]
        return cls.sm2_intervals_sec[box]

    @classmethod
    def get_next_session_interval_days(cls, box: int) -> int:
        """
        SM2 staggered intervals (powers of 1.7) days. (Rounded up to the next whole day).
        :param box:
        :return:
        """
        if box < 0:
            return cls.sm2_intervals_days[0]
        if box >= len(cls.sm2_intervals_days):
            return cls.sm2_intervals_days[-1]
        return cls.sm2_intervals_days[box]

    @classmethod
    def init(cls):
        sec: float
        if not cls.pimsleur_intervals_sec:
            cls.pimsleur_intervals_sec = []
            sec = 1
            for _ in range(15):
                sec *= 5
                cls.pimsleur_intervals_sec.append(sec)

        days: float
        if not cls.sm2_intervals_sec:
            cls.sm2_intervals_sec = []
            secs_day = 60.0 * 60.0 * 24.0
            cls.sm2_intervals_sec.append(secs_day)
            days = 4.0
            for _ in range(15):
                cls.sm2_intervals_sec.append(days * secs_day)
                days *= 1.7

        if not cls.sm2_intervals_days:
            days = 4.0
            cls.sm2_intervals_days = []
            for _ in range(15):
                cls.sm2_intervals_days.append(math.ceil(days))
                days *= 1.7


