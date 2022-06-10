import math


class LeitnerCardUtils:

    def __init__(self):
        pass

    pimsleur_intervals_sec: list[float] = None
    sm2_intervals_sec: list[float] = None
    sm2_intervals_days: list[int] = None

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

    init()
