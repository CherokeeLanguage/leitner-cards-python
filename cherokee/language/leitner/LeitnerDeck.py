from .LeitnerCard import LeitnerCard


class LeitnerDeck(list):

    def __init__(self):
        super().__init__()
        self.cards: list[LeitnerCard] = []

