# from cherokee.language.leitner.LeitnerCardStats import LeitnerCardStats
from .LeitnerCardStats import LeitnerCardStats
from .LeitnerDeck import LeitnerDeck


class LeitnerCard:

    def __init__(self):
        self.stats: LeitnerCardStats = LeitnerCardStats()
        self.deck: LeitnerDeck = None

    def __lt__(self, other):

        pass

