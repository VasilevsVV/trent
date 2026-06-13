class MissingValueException(Exception):
    def __init__(self, val, fn_name: str) -> None:
        self._value = val
        self._fn_name = fn_name

    def __str__(self) -> str:
        return f'Missing {self._fn_name} for value: {self._value}'


class EmptyCollectionException(Exception):
    def __init__(self, msg: str) -> None:
        self.__msg = msg

    def __str__(self) -> str:
        return f'Collection is empty! {self.__msg}'