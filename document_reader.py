from PyPDF2 import PdfReader
from config import DOCUMENTS_DIRECTORY
from os import path, listdir
from typing import List, Tuple

# Read text from a pdf file
def read_pdf(file_path: str) -> str:
    pdf_file = open(file_path, 'rb')
    read_pdf = PdfReader(pdf_file)
    
    # concatenate all pages' text
    full_text = " ".join([page.extract_text() for page in read_pdf.pages])

    return full_text

def clean_texts(texts: List[str]) -> List[str]:
    cleaned_texts = texts
    # replace new line with space
    cleaned_texts = map(lambda text: text.replace('\n', ' '), cleaned_texts)
    # replace multiple spaces with one space
    cleaned_texts = map(lambda text: ' '.join(text.split()), cleaned_texts)
    # reassemble splitted words
    cleaned_texts = map(lambda text: text.replace('- ', ''), cleaned_texts)

    return list(cleaned_texts)

###################################################################################################
### Read and Process the Files ####################################################################
###################################################################################################

def read_pdfs_and_get_texts() -> Tuple[List[str], List[str], List[str]]:
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

if __name__ == '__main__':
    _, _, texts = read_pdfs_and_get_texts()