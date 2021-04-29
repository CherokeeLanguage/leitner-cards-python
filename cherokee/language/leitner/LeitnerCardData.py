from abc import abstractmethod
from functools import total_ordering


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
    

