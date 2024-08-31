from typing import Any, Generic, Iterable, Iterator, Optional, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')

class abc_node(ABC, Generic[T]):
    def __init__(self, val: T, *,
                 left = None, right = None) -> None:
        self.__val: T
        # self.left: Any
        # self.right: Any
        super().__init__()
    
    @property
    @abstractmethod
    def value(self) -> T: ...
    
    @property
    @abstractmethod
    def left(self) -> Any: ...
    
    @left.setter
    def left(self, left) -> None: ...
    
    @property
    @abstractmethod
    def right(self) -> Any: ...
    
    @right.setter
    @abstractmethod
    def right(self, right) -> None: ...
    
    @abstractmethod
    def __repr__(self) -> str:
        return super().__repr__()


class NodeIter(Iterable[T]):
    def __init__(self, pointer: Optional[abc_node[T]]) -> None:
        self.__head: Optional[abc_node[T]] = pointer
    
    
    def __iter__(self):
        return self
    
    def __next__(self) -> T:
        if self.__head is None:
            raise StopIteration
        __val = self.__head.value
        self.__head = self.__head.right
        return __val


class node(abc_node, Generic[T]):
    def __init__(self, val: T, *,
                 left: Optional[abc_node] = None,
                 right: Optional[abc_node] = None) -> None:
        self.__val: T = val
        self.__val_type = type(val)
        self.__left: Optional[abc_node] = left
        self.__right: Optional[abc_node] = right
        
    
    @property
    def value(self) -> T:
        return self.__val
    
    @property
    def left(self):
        return self.__left
    
    @left.setter
    def left(self, left: abc_node):
        assert isinstance(left, abc_node), "'left' type MUST be node"
        self.__left = left
    
    @property
    def right(self):
        return self.__right
    
    @right.setter
    def right(self, right: abc_node):
        assert isinstance(right, abc_node), "'right' type MUST be node"
        self.__right = right
    
    def __repr__(self) -> str:
        res = f'[{self.__val}]'
        if self.__right:
            res += '->' + str(self.right)
        return res
    
    def __iter__(self) -> Iterable[T]:
        return NodeIter(self)



class dllist(Iterable[T]):
    def __init__(self, lst: Optional[Iterable[T]] = None) -> None:
        self.__head: Optional[node[T]] = None
        self.__tail: Optional[node[T]] = None
        self.__pointer: Optional[node[T]] = None
        if lst is not None:
            for el in lst:
                self.append(el)
    
    def append(self, value: T) -> T:
        n = node(value)
        if self.__head is None or self.__tail is None:
            self.__head = n
            self.__tail = n
            return value
        self.__tail.right = n
        self.__tail = n
        return value
    
    
    def __repr__(self) -> str:
        res = 'dllist('
        if self.__head:
            res += f'{self.__head.value}'
            if self.__head.right:
                for el in NodeIter(self.__head.right):
                    res += f', {el}'
        res += ')'
        return res
    
    def __iter__(self) -> Iterator[T]:
        return NodeIter(self.__head)


if __name__ == '__main__':
    lst = dllist([1,2,3])
    print(lst)
    lst.append(4)
    print(lst)
    print(dllist())