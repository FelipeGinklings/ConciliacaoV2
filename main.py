from typing import Dict, List
import PyPDF2
import tkinter as tk
from tkinter import filedialog
from utils import CreateFile, Item, Result


def file_name():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title='Escolha o PDF para análise')
    return file_path


def write_path():
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
    next_data = get_data(position_valor+1, pdf_list)
    next_data.append(data)
    return next_data


def group_data(raw_data: List[Item]):
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


def hidrate_data(data: Dict[str, List[Item]]):
    total = 0
    paid = 0
    difference = 0
    complement = 0
    for item in data['items']:
        item: Item
        if item.hist == 20:
            difference += item.value
            total += item.value
        elif item.hist == 133:
            difference -= item.value
            paid += item.value
        complement = item.complement

    data['results'] = Result(
        complement=complement,
        total=round(total, 2),
        paid=round(paid, 2),
        difference=round(difference, 2),
    )
    return data


def final_result(data):
    totals = 0
    payments = 0
    differences = 0

    for item in data.values():
        totals += item.total
        payments += item.paid
        differences += item.difference

    finalresult = Result(
        complement='Resultado Final',
        total=totals,
        paid=payments,
        difference=differences,
    )
    return finalresult


def separate_data(grouped_data):
    next_year = {}
    paid = {}
    not_paid = {}
    last_year = {}

    for items in grouped_data.values():
        result: Result = items['results']

        # Pagamento do Ano Anterior
        if result.difference < 0:
            last_year[result.complement] = result
        # Pagamento Completo
        elif result.difference == 0:
            paid[result.complement] = result
        # Pagamento Incompleto
        elif result.difference > 0 and result.paid > 0:
            not_paid[result.complement] = result
        # Pagamento Próximo
        elif result.paid == 0:
            next_year[result.complement] = result

    next_year['final result'] = final_result(next_year)
    paid['final result'] = final_result(paid)
    not_paid['final result'] = final_result(not_paid)
    last_year['final result'] = final_result(last_year)

    return not_paid, paid, next_year, last_year


def main():
    # file_name = 'teste.pdf'
    filename = file_name()
    if not filename:
        return 0
    pdf_list = pdf_to_list(filename)
    raw_data = get_data(0, pdf_list)
    grouped_data, grouped_error = group_data(raw_data)
    writepath = write_path()
    # write_path = "/home/felipe/Documentos/VSCodeProjetos/Conciliação de Notas/ConciliacaoV2/Resultados"
    if not writepath:
        return 0
    create_file = CreateFile(writepath)
    if grouped_error:
        create_file.write_file("ERROR", grouped_error)
    for items in grouped_data.values():
        items = hidrate_data(items)

    not_paid, paid, next_year, last_year = separate_data(grouped_data)
    if not_paid or paid or not next_year or last_year:
        create_file.write_file("NOT PAID", not_paid)
        create_file.write_file("PAID", paid)
        create_file.write_file("NEXT YEAR", next_year)
        create_file.write_file("LAST YEAR", last_year)


if __name__ == '__main__':
    main()