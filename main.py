from typing import List
import PyPDF2


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


pdf_list = pdf_to_list()


def get_complement(p_complemento, p_complemento_end):
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


def get_data(start: int = 0):
    try:
        position_valor = pdf_list.index('Valor', start)
        position_hist = pdf_list.index('Hist', position_valor)
        position_complemento = pdf_list.index('Complemento', position_hist)
        position_complemento_end = pdf_list.index('*', position_complemento)
    except ValueError:
        return []
    value = float(
        pdf_list[position_valor+2].replace('.', '').replace(',', '.'))
    hist = int(pdf_list[position_hist+2])
    has_error, complement = get_complement(
        position_complemento, position_complemento_end)


def main():
    file_name = 'teste.pdf'
    if not file_name:
        return 0
    pdf_to_list(file_name)


if __name__ == '__main__':
    main()
