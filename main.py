from typing import List, Item
import PyPDF2
import tkinter as tk
from tkinter import filedialog
import os


def name_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title='Escolha o PDF para análise')
    file_name = os.path.basename(file_path)
    return file_path


def path_end():
    root = tk.Tk()
    root.withdraw()

    end = filedialog.askdirectory(
        title='Escolha onde os arquivos serão exportados')
    return end

def pdf_to_list(filename: str = 'teste.pdf'):

    pdf_file = open(filename, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    total_text = ''

    for i in range(num_pages):
        page = pdf_reader.pages[i]
        text = page.extract_text()
        positions_end_line = [n for n, v in enumerate(text) if v == '\n']
        for nn in positions_end_line:
            text = list(text)
            text[nn] = ' * '
        text = ''.join(text)
        total_text += text

    return total_text.split()


def get_complement(p_complemento: int, p_complemento_end: int, pdf_list: List[str]):
    try:
        complement = int(pdf_list[p_complemento+2])
    except ValueError:
        extract_complement_number = [
            n for n in pdf_list[p_complemento:p_complemento_end] if n.isnumeric()]
        if not extract_complement_number:
            complement = ' '.join(pdf_list[p_complemento:p_complemento_end])
            return (True, complement)
        complement = int(extract_complement_number[0])
    return (False, complement)


def get_data(start: int = 0, pdf_list: List[str] = []):
    try:
        position_valor = pdf_list.index('Valor', start)
        position_hist = pdf_list.index('Hist', position_valor)
        position_complemento = pdf_list.index('Complemento', position_hist)
        position_complemento_end = pdf_list.index('*', position_complemento)
    except ValueError:
        print()
        return []
    value = float(
        pdf_list[position_valor+2].replace('.', '').replace(',', '.'))
    hist = int(pdf_list[position_hist+2])
    has_error, complement = get_complement(
        position_complemento, position_complemento_end, pdf_list)

    data = Item(
        value=value,
        hist=hist,
        has_error=has_error,
        complement=complement,
    )


    # Não passa daqui até ele chegar no final
    # next_data é uma função dentro da função em loop
    next_data = get_data(position_valor+1, pdf_list)
    next_data.append(data)
    return next_data

def group_data(raw_data:List[Item]):
    grouped_data = {}
    grouped_error: List[Item] = []
    for item in raw_data:
        if item.has_error:
            grouped_error.append(item)
        else:
            if item.complement not in grouped_data:
                grouped_data[item.complement] = {
                    'items': [item]
                }
            else:
                grouped_data[item.complement]['items'].append(item)
    return grouped_data, grouped_error


def main():
    file_name = 'teste.pdf'
    if not file_name:
        return 0
    pdf_list = pdf_to_list(file_name)
    raw_data = get_data(0, pdf_list)
    grouped_data, grouped_error = group_data(raw_data)
    write_path = "/home/felipe/Documentos/VSCodeProjetos/Conciliação de Notas/V2/Resultados"
    if not write_path:
        return 0 


if __name__ == '__main__':
    main()
