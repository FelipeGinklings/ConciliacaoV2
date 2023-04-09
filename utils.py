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
