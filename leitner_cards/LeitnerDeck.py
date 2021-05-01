from abc import abstractmethod
from collections import MutableSequence
from typing import Iterable
from typing import overload

from .LeitnerCard import LeitnerCard


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
