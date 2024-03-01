from test_and_debug_utils import get_test_texts
from sentence_transformers import SentenceTransformer
import numpy as np
from torch import dist, flatten
from faiss import IndexIDMap, IndexFlatL2, read_index, write_index
from os import path, getcwd, makedirs, listdir, remove
from PyPDF2 import PdfReader
from sqlite3 import connect
import nltk

DOCUMENTS_DIRECTORY = path.join(getcwd(), 'documents')
DATABASES_DIRECTORY = path.join(getcwd(), 'databases')

config = {
    'model': 'all-MiniLM-L6-v2',
    'dimension': 384,
}

model = SentenceTransformer(config['model'])

# TODO: properly implement
class VectorDatabase:
    def __init__(self, index_name: str):
        index_directory = DATABASES_DIRECTORY

        # Create the directory to store the index if it doesn't exist
        if not path.exists(index_directory):
            makedirs(index_directory)
        
        # get the path to store the index to
        self._index_path = path.join(index_directory, index_name)

        if path.isfile(self._index_path):
            self._index = read_index(self._index_path)
            # TODO: Do we get an exception if the index file is not valid?
        else:
            self._index = IndexIDMap(IndexFlatL2(config['dimension']))

    def store_vector(self, identifier: int, vector: np.ndarray):
        self._index.add_with_ids(np.array([vector]), np.array([identifier]))
    
    def build_index(self):
        if self._index.is_trained:
            print("Index is already trained")
        else:
            print("Training index...")
            self._index.train(self._vector_list)
            print("Index trained")
    
    def save_database_to_disk(self):
        # the index is not written to disk immediately
        write_index(self._index, self._index_path)
        

    def get_nearest_neighbors_ids_and_distances(self, embedding_vector, n_neighbors: int):
        D, I = self._index.search(np.array([embedding_vector]), n_neighbors)
        return I[0], D[0]

# TODO: properly implement
class ContentDatabase:
    def __init__(self, database_name: str):
        database_directory = DATABASES_DIRECTORY

        # Create the directory to store the index if it doesn't exist
        if not path.exists(database_directory):
            makedirs(database_directory)
        
        # connect to database
        self._database_path = path.join(database_directory, database_name)
        self._con = connect(self._database_path)
        self._initialize_database()

        self._identifiers = []
        self._sentences = []

    def _initialize_database(self):
        cur = self._con.cursor()
        # check if database is already setup
        required_tables = ['document', 'sentence']
        all_tables_exist = True
        for table_name in required_tables:
            res = cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?", (table_name,))
            document_table_exists = res.fetchone()
            all_tables_exist = all_tables_exist and bool(document_table_exists is not None)

        if all_tables_exist:
            # assume database was correctly initialized and return
            cur.close()
            return
        
        print("Not all database tables found as expected. Create database tables...")

        cur.execute("CREATE TABLE document (id INTEGER PRIMARY KEY, title TEXT, path TEXT)")
        cur.execute("CREATE TABLE sentence (id INTEGER PRIMARY KEY, document_id INTEGER, sentence_number INTEGER, content TEXT)")
        self._con.commit()
        cur.close()

    def get_documents_in_db(self):
        cur = self._con.cursor()
        res = cur.execute("SELECT id, title, path FROM document")
        documents = res.fetchall()
        cur.close()
        return documents

    def get_next_free_id(self):
        cur = self._con.cursor()
        res = cur.execute("SELECT max(id) from sentence")
        (max_identifier,) = res.fetchone()
        return max_identifier + 1 if max_identifier is not None else 1
    
    def store_document_data(self, identifier: int, title: str, path: str):
        cur = self._con.cursor()
        cur.execute("INSERT INTO document VALUES (?, ?, ?)", (identifier, title, path))
        self._con.commit()
        cur.close()

    def store_sentence_data(self, identifier: int, sentence_content: str, document_id: str, sentence_number: int):
        cur = self._con.cursor()
        cur.execute("INSERT INTO sentence VALUES (?, ?, ?, ?)", (identifier, document_id, sentence_number, sentence_content))
        self._con.commit()
        cur.close()

    def get_sentence_data(self, identifier: int):
        cur = self._con.cursor()
        res = cur.execute("SELECT d.title, s.sentence_number, s.content FROM sentence s LEFT JOIN document d ON s.document_id = d.id WHERE s.id = ?", (identifier,))
        document, sentence_number, content = res.fetchone()
        return {'document': document,
                'sentence_number': sentence_number,
                'sentence_content': content,
                }

    def get_sentences_by_document_id(self, document_id: int):
        cur = self._con.cursor()
        res = cur.execute("SELECT id, document_id, sentence_number, content FROM sentence WHERE document_id = ? ORDER BY sentence_number", (document_id,))
        sentences = res.fetchall()
        result = []
        for id, document_id, sentence_number, content  in sentences:
            result.append({'id': id,
                           'document_id': document_id,
                           'sentence_number': sentence_number,
                           'content': content
                           })
        cur.close()
        return result

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
        content_db_path = path.join(DATABASES_DIRECTORY, content_db_name)
        remove(content_db_path)

        vector_db_path = path.join(DATABASES_DIRECTORY, vector_db_name)
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

