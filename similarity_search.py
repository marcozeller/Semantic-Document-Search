from test_and_debug_utils import get_test_texts
from sentence_transformers import SentenceTransformer
import numpy as np
from torch import dist, flatten
from faiss import IndexIDMap, IndexFlatL2

config = {
    'model': 'all-MiniLM-L6-v2',
    'dimension': 384,
}

model = SentenceTransformer(config['model'])

# TODO: properly implement
class VectorDatabase:
    def __init__(self, path: str):
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

    def get_nearest_neighbors_ids(self, embedding_vector, n_neighbors: int):
        D, I = self._index.search(np.array([embedding_vector]), n_neighbors)
        return I[0]

# TODO: properly implement
class ContentDatabase:
    def __init__(self, path: str):
        self._identifiers = []
        self._sentences = []

    def get_next_free_id(self):
        return 1 if len(self._identifiers) == 0 else max(self._identifiers) + 1

    def store_sentence_data(self, identifier: int, sentence_content: str, document: str, sentence_number: int):
        self._identifiers.append(identifier)
        self._sentences.append({'document': document,
                                'sentence_number': sentence_number,
                                'sentence_content': sentence_content,
                                'distance': 0.5 # TODO: this should not be derived from here...
                                })

    def get_sentence_data(self, identifier: int):
        index = self._identifiers.index(identifier)
        return self._sentences[index]

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

# Some global state will be moved into a database at some point
documents, texts = get_test_texts()
texts = clean_texts(documents, texts)
   
def get_similar_sentences(target_sentence, num_results=10):
    final_sentences = []
    final_docs = []
    final_sentence_numbers = []

    for doc, text in zip(documents, texts):
        sentences = text.split(".")
        for sentence_number, sentence in enumerate(sentences):
            if len(sentence) > 10:
                final_sentences.append(sentence)
                final_docs.append(doc)
                final_sentence_numbers.append(sentence_number)
    
    final_sentences.append(target_sentence)
    final_embeddings = model.encode(final_sentences, convert_to_tensor=True)
    target_embedding = flatten(final_embeddings[-1])

    vector_database = VectorDatabase('vector_database.vec')
    content_database = ContentDatabase('content_database.db')

    for sentence, doc, sentence_number, embedding in zip(final_sentences, final_docs, final_sentence_numbers, final_embeddings):
        identifier = content_database.get_next_free_id()

        vector_database.store_vector(identifier, embedding)
        content_database.store_sentence_data(identifier, sentence, doc, sentence_number)
    
    vector_database.build_index()
    nearest_neighbors_ids = vector_database.get_nearest_neighbors_ids(target_embedding, num_results)

    sentences_data = [content_database.get_sentence_data(identifier) for identifier in nearest_neighbors_ids]

    return sentences_data

    """
    final_corpus = [{'sentence_content': sentence,
                     'document': doc,
                     'sentence_number': sentence_number,
                     'distance': float(dist(flatten(embedding), target_embedding))}
                     for sentence, doc, sentence_number, embedding
                     in zip(final_sentences, final_docs, final_sentence_numbers, final_embeddings)] 


    final_corpus.sort(key=lambda x: x["distance"], reverse=False)

    return final_corpus[:num_results]
    """

if __name__ == "__main__":
    test_sentence = "The fox is a lovely animal."
    print(get_similar_sentences(test_sentence, 3))

