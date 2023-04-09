from typing import List
import PyPDF2


def pdf_to_list(filename:str='teste.pdf'):
    
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




def main():
    file_name = 'teste.pdf'
    if not file_name:
        return 0
    pdf_to_list(file_name)
    
if __name__ == '__main__':
    main()