from PyPDF2 import PdfReader
from config import DOCUMENTS_DIRECTORY
from os import path, listdir
from typing import List, Tuple

class FileProcessor:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.file_path = path.join(DOCUMENTS_DIRECTORY, file_name)
    
    def read_full_text():
        """
        Subclasesses have to override this function to parse and extract text from a specific file-type or using a specific strategy.
        The extracted text needs to be stored in self.full_text to ensure proper working.
        """
        raise NotImplementedError("Subclass needs to implement read_full_text() method")
        
    def clean_full_text(self):
        if not self.full_text:
            self.read_full_text()

        self.cleaned_text = self.full_text
        # replace new line with space
        self.cleaned_text = self.cleaned_text.replace('\n', ' ')
        # replace multiple spaces with one space
        self.cleaned_text = ' '.join(self.cleaned_text.split())
        # reassemble splitted words
        self.cleaned_text = self.cleaned_text.replace('- ', '')

class PdfProcessor(FileProcessor):
    # Read text from a pdf file
    def read_full_text(self):
        pdf_file = open(self.file_path, 'rb')
        read_pdf = PdfReader(pdf_file)

        # concatenate all pages' text
        self.full_text = " ".join([page.extract_text() for page in read_pdf.pages])

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
        pdf_file_processor = PdfProcessor(file_name)
        pdf_file_processor.read_full_text()
        pdf_file_processor.clean_full_text()

        file_paths.append(pdf_file_processor.file_path)
        file_names.append(pdf_file_processor.file_name)
        texts.append(pdf_file_processor.cleaned_text)
    
    return file_paths, file_names, texts

if __name__ == '__main__':
    _, _, texts = read_pdfs_and_get_texts()
    print(texts)