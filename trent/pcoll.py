from typing import Iterable, Optional, TypeVar
from trent.coll import NestedIterationExceprion, icoll

T = TypeVar('T')

class pcoll(icoll, Iterable[T]):
    def __init__(self, collection: Optional[Iterable[T]] = None) -> None:
        self.__buffer: list[T]
        super().__init__(collection)
    
    
    def __iter__(self):
        if self.__is_iterated:
            raise NestedIterationExceprion
        self.__buffer = []
        self.__iter = iter(self.__coll)
        self.__is_iterated = True
        return self
    
    
    def __next__(self) -> T:
        try:
            val = next(self.__iter)
        except StopIteration:
            self.__coll = self.__buffer
            self.__is_iterated = False
            raise StopIteration
        self.__buffer.append(val)
        return val