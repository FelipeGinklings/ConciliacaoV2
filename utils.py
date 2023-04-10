from dataclasses import dataclass
from typing import Union, Dict, List
import os


@dataclass
class Item:
    value: float
    hist: int
    complement: Union[str, int]
    has_error: bool

    @property
    def formated_value(self):
        return '{:.2f}'.format(self.value).replace('.', ',')


@dataclass
class Result:
    complement: int
    total: float
    paid: float
    difference: float


class SelectorNotFound(Exception):

    def __init__(self):
        message = "Selector not found"
        super.__init__(message)


class CreateFile():

    SELECTORS = {
        'PAA': {
            'filename': 'Pagamentos Ano Anterior.txt',
            'header': 'Aqui estão listados todos os pagamentos de notas do ano passado:'
        },
        'PC': {
            'filename': 'Pagamentos Completos.txt',
            'header': 'Aqui estão as notas desse ano que foram completamente pagas:'
        },
        'PI': {
            'filename': 'Pagamentos Incompletos.txt',
            'header': 'Aqui estão as notas desse ano que não foram completamente pagas:'
        },
        'PAS': {
            'filename': 'Somente Pagamentos do Ano Subsequente.txt',
            'header': 'Aqui estão as notas a serem pagas no próximo ano:'
        },
        'ERROR': {
            'filename': 'Erros nos complementos.txt',
            'header': 'Aqui estão as notas com erros de nomenclatura:'
        }
    }

    def __init__(self, path):
        self.path = path

    def write_file(self, selector: str, data):
        selected = self.SELECTORS.get(selector)
        if not selected:
            raise SelectorNotFound()

        filename = selected['filename']
        header = selected['header']
        full_path = os.path.join(self.path, filename)
        with open(full_path, 'w') as file:
            file.write(header)
            file.write('\n\n')

            if selector == 'ERROR':
                self.__write_erros(file, data)
            else:
                self.__write_items(file, data)

    def __write_erros(self, file, data):
        for index, item in enumerate(data):
            item: Item
            file.writelines([
                f"Erro: {index+1}\n",
                f"Complemento: {item.complement}\n",
                f"Valor: {item.formated_value}\n",
                "\n"
            ])
