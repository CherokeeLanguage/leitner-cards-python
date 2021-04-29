import math

from cherokee.language.leitner.LeitnerCardStats import LeitnerCardStats
from cherokee.language.leitner.LeitnerDeck import LeitnerDeck
from cherokee.language.leitner.LeitnerSkillLevel import LeitnerSkillLevel


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
