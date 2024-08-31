from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable, Iterator, Optional, TypeVar

T = TypeVar('T')
T1 = TypeVar('T1')

class _coll(ABC, Iterable[T]):
    @abstractmethod
    def map(self, f: Callable[[T], T1]) -> Any:...
    
    @property
    @abstractmethod
    def collection(self) -> Iterable[T]: ...
    
    @abstractmethod
    def __iter__(self) -> Iterator[T]: ...
    
    @abstractmethod
    def __next__(self) -> T: ...
    
    @abstractmethod
    def __repr__(self) -> str: ...

class NestedIterationExceprion(Exception):
    def __repr__(self) -> str:
        return 'Nested iteration over `coll` class is invalid !!!'



class coll(_coll, Iterable[T]):
    def __init__(self, collection: Optional[Iterable[T]] = None) -> None:
        self.__coll: Iterable[T]
        self.__buffer: list[T]
        self.__iter: Iterator[T]
        self.__is_iterated: bool = False
        if collection is not None:
            self.__coll = collection
        else:
            self.__coll = []
    
    @property
    def collection(self) -> Iterable[T]:
        return self.__coll
    
    def map(self, f: Callable[[T], T1]) -> _coll[T1]:
        return coll(map(f, self.__coll))
    
    
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
            raise StopIteration
        self.__buffer.append(val)
        return val
    
    def __repr__(self) -> str:
        lst = list(self)
        return f'coll({lst})'


if __name__ == '__main__':
    c = coll([1,2,3,4]).map(lambda x: x+1)