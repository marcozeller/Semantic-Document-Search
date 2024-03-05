from test_and_debug_utils import get_test_texts
from sentence_transformers import SentenceTransformer
from os import path, listdir, remove
from PyPDF2 import PdfReader
import nltk

from config import DOCUMENTS_DIRECTORY, DATABASES_DIRECTORY, model_config
from vector_database import VectorDatabase
from content_database import ContentDatabase

model = SentenceTransformer(model_config['model'])

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

def clean_texts(documents, texts):
    # Clean texts
    for i in range(len(documents)):
        text = texts[i]
        # replace new line with space
        text = text.replace('\n', ' ')
        # replace multiple spaces with one space
        text = ' '.join(text.split())
        # reassemble splitted words
        text = text.replace('- ', '')

        texts[i] = text
    
    return texts

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
    
    return file_paths, file_names, texts

def rebuild_databases(content_db_name, vector_db_name, delete_databases):
    if delete_databases:
        # remove database files only if they already exist
        content_db_path = path.join(DATABASES_DIRECTORY, content_db_name)
        if path.isfile(content_db_path):
            remove(content_db_path)

        vector_db_path = path.join(DATABASES_DIRECTORY, vector_db_name)
        if path.isfile(vector_db_path):
            remove(vector_db_path)
        
    file_paths, file_names, texts = read_pdfs_and_get_texts()
    texts = clean_texts(file_names, texts)

    final_sentences = []
    final_doc_ids = []
    final_sentence_numbers = []
    document_metadata = []

    for doc_id, (doc_title, doc_path, doc_content) in enumerate(zip(file_names, file_paths, texts)):
        document_metadata.append((doc_id, doc_title, doc_path))
        sentences = nltk.sent_tokenize(doc_content)
        #sentences = doc_content.split(".")
        for sentence_number, sentence in enumerate(sentences):
            if len(sentence) > 10:
                final_sentences.append(sentence)
                final_doc_ids.append(doc_id)
                final_sentence_numbers.append(sentence_number)
    
    final_embeddings = model.encode(final_sentences, convert_to_tensor=True)

    vector_database = VectorDatabase('vector_database.vec')
    content_database = ContentDatabase('content_database.db')

    # comment in to build database when run the first time
    for doc_id, doc_title, doc_path in document_metadata:
        content_database.store_document_data(doc_id, doc_title, doc_path)

    for sentence, doc_id, sentence_number, embedding in zip(final_sentences, final_doc_ids, final_sentence_numbers, final_embeddings):
        identifier = content_database.get_next_free_id()

        vector_database.store_vector(identifier, embedding)
        content_database.store_sentence_data(identifier, sentence, doc_id, sentence_number)
    vector_database.build_index()
    vector_database.save_database_to_disk()

   
def get_similar_sentences(target_sentence, num_results=10):
    target_embedding = model.encode(target_sentence, convert_to_tensor=True)

    vector_database = VectorDatabase('vector_database.vec')
    content_database = ContentDatabase('content_database.db')

    nearest_neighbors_ids, nearest_neighbors_distances = vector_database.get_nearest_neighbors_ids_and_distances(target_embedding, num_results)

    sentences_data = [content_database.get_sentence_data(int(identifier)) for identifier in nearest_neighbors_ids]
    for sentence_data, nn_dist in zip(sentences_data, nearest_neighbors_distances):
        sentence_data['distance'] = float(nn_dist)

    return sentences_data

def get_documents_in_db():
    content_database = ContentDatabase('content_database.db')
    documents_in_db = content_database.get_documents_in_db()
    result = []
    for identifier, title, path in documents_in_db:
        document_entry = { "identifier": identifier, "title": title, "path": path}
        result.append(document_entry)

    return result

def get_document_content_by_id(document_id):
    content_database = ContentDatabase('content_database.db')
    sentences = content_database.get_sentences_by_document_id(document_id)
    return sentences

if __name__ == "__main__":
    rebuild_databases('content_database.db', 'vector_database.vec', True)

    test_sentence = "The fox is a lovely animal."
    print(get_similar_sentences(test_sentence, 3))

