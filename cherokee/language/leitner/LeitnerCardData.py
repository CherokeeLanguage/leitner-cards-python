from abc import abstractmethod


class LeitnerCardData:
    def __init__(self):
        pass

    @abstractmethod
    def id(self) -> str: ...

    @abstractmethod
    def sort_key(self) -> str: ...
    

