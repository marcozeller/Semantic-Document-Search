from test_and_debug_utils import get_test_texts
from sentence_transformers import SentenceTransformer
from os import path, remove
import nltk

from config import DATABASES_DIRECTORY, model_config
from vector_database import VectorDatabase
from content_database import ContentDatabase
from document_reader import read_pdfs_and_get_texts

model = SentenceTransformer(model_config['model'])


###################################################################################################
### Build the Databases ###########################################################################
###################################################################################################

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

    #sentences = [nltk.sent_tokenize(full_text) for full_text in texts]

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

    for doc_id, doc_title, doc_path in document_metadata:
        content_database.store_document_data(doc_id, doc_title, doc_path)

    #for sentence, doc_id, sentence_number, embedding in zip(final_sentences, final_doc_ids, final_sentence_numbers, final_embeddings):

    identifiers = content_database.get_next_free_ids(len(final_sentences))

    vector_database.store_vectors(identifiers, final_embeddings)
    content_database.store_sentence_data_batch(identifiers, final_sentences, final_doc_ids, final_sentence_numbers)
    vector_database.build_index()
    vector_database.save_database_to_disk()

###################################################################################################
### Query the existing data from the databases ####################################################
###################################################################################################
   
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

