import numpy as np
from os import path, makedirs
from faiss import IndexIDMap, IndexFlatL2, read_index, write_index
from typing import List

from config import DATABASES_DIRECTORY, model_config

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
            self._index = IndexIDMap(IndexFlatL2(model_config['dimension']))

    def store_vector(self, identifier: int, vector: np.ndarray):
        self._index.add_with_ids(np.array([vector]), np.array([identifier]))

    def store_vectors(self, identifiers: List[int], vectors: np.ndarray):
        self._index.add_with_ids(np.array(vectors), np.array(identifiers))
    
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