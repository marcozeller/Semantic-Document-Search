from PyPDF2 import PdfReader
from config import DOCUMENTS_DIRECTORY
from os import path, listdir

# Read text from a pdf file
def read_pdf(file_path):
    pdf_file = open(file_path, 'rb')
    read_pdf = PdfReader(pdf_file)
    number_of_pages = len(read_pdf.pages)
    text = []
    for page_number in range(number_of_pages):
        page = read_pdf.pages[page_number]
        page_content = page.extract_text()
        text.append(page_content)
    return " ".join(text)

def clean_texts(texts):
    cleaned_texts = []
    # Clean texts
    for text in texts:
        cleaned_text = text
        # replace new line with space
        cleaned_text = cleaned_text.replace('\n', ' ')
        # replace multiple spaces with one space
        cleaned_text = ' '.join(cleaned_text.split())
        # reassemble splitted words
        cleaned_text = cleaned_text.replace('- ', '')
        cleaned_texts.append(cleaned_text)

    return cleaned_texts

###################################################################################################
### Read and Process the Files ####################################################################
###################################################################################################

def read_pdfs_and_get_texts():
    file_names = []
    file_paths = []
    texts = []
    for file_name in listdir(DOCUMENTS_DIRECTORY):
        if not file_name.endswith('.pdf'):
            continue
        print(file_name)
        file_path = path.join(DOCUMENTS_DIRECTORY, file_name)

        file_paths.append(file_path)
        file_names.append(file_name)
        texts.append(read_pdf(file_path))
    
    return file_paths, file_names, clean_texts(texts)