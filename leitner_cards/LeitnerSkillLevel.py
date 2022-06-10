from enum import Enum


class LeitnerSkillLevel(Enum):
    def __init__(self):
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
    def get_next(cls, level=None) -> 'LeitnerSkillLevel':
        if not level:
            return LeitnerSkillLevel.NEWBIE
        return level.next()

    def get_achievement_points(self) -> int:
        return self.value[1] * 5

    def get_english(self) -> str:
        return self.value[0]

    def get_level(self) -> int:
        return self.value[1]

    def next(self):
        return LeitnerSkillLevel.for_level(self.get_level()+1)

    def __str__(self)->str:
        return self.get_english()
