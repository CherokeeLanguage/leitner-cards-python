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

    def pimsleur_box_dec(self)->None:
        if self.pimsleur_box > 0:
            self.pimsleur_box -= 1

    def pimsleur_box_inc(self)->None:
        self.pimsleur_box += 1

    def tries_remaining_dec(self)->None:
        if self.tries_remaining > 0:
            self.tries_remaining -= 1

    def tries_remaining_inc(self)->None:
        self.tries_remaining += 1

    def has_tries_remaining(self)->bool:
        return self.tries_remaining > 0

