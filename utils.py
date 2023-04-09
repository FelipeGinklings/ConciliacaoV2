from dataclasses import dataclass
from typing import Union


@dataclass
class Item:
    value: float
    hist: int
    complement: Union[str, int]
    has_error: bool

    @property
    def formated_value(self):
        return '{:.2f}'.format(self.value).replace('.', ',')


class SelectorNotFound(Exception):

    def __init__(self):
        message = "Selector not found"
        super.__init__(message)
