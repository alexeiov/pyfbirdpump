import PyPDF2
from file_path_getter import get_path

data_file = get_path()
with open(data_file, 'rb') as pdfObj:
    pdfReader = PyPDF2.PdfFileReader(pdfObj)
    num_pages = pdfReader.numPages
    for page_num in range(num_pages):
        pageObj = pdfReader.getPage(page_num)
        # print(pageObj.extractText())
        contents = pageObj.extractText()
        with open('data_from_pdf.txt', 'a', encoding='utf8') as extractedText:
            extractedText.write(contents)