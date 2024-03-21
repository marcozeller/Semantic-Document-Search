from os import path, makedirs
from sqlite3 import connect
from typing import List

from config import DATABASES_DIRECTORY

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

    def _initialize_database(self) -> None:
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

    def get_next_free_id(self) -> int:
        """
        Returns the next free identifier in the database.
        Any identifier larger or equal than the one returned is guaranteed to be free.
        """
        cur = self._con.cursor()
        res = cur.execute("SELECT max(id) from sentence")
        (max_identifier,) = res.fetchone()
        return max_identifier + 1 if max_identifier is not None else 1

    def get_next_free_ids(self, n_ids: int) -> List[int]:
        """
        Returns a list of length specified in the parameter of free identifiers.
        There is no lock on the identifiers, so they might be taken by another process in the meantime.
        """
        # TODO: In a multiple user scenario (which we do not have yet), inserting into both databases needs to be atomic.
        # Implement locking accross all components as database transactions alone will not be enough to guarantee consistency.

        cur = self._con.cursor()
        res = cur.execute("SELECT max(id) from sentence")
        (max_identifier,) = res.fetchone()

        # start id might not be the first free id, but any id higher or equal to it is guaranteed to be free
        start_id = max_identifier + 1 if max_identifier is not None else 1
        
        return [start_id + i for i in range(n_ids)]
    
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

    def store_sentence_data_batch(self, identifiers: List[int], sentence_contents: List[str], document_ids: List[str], sentence_numbers: List[int]):
        cur = self._con.cursor()
        cur.executemany("INSERT INTO sentence VALUES (?, ?, ?, ?)", list(zip(identifiers, document_ids, sentence_numbers, sentence_contents)))
        self._con.commit()
        cur.close()

    def get_sentence_data(self, identifier: int):
        cur = self._con.cursor()
        res = cur.execute("SELECT s.document_id, d.title, s.sentence_number, s.content FROM sentence s LEFT JOIN document d ON s.document_id = d.id WHERE s.id = ?", (identifier,))
        document_id, document, sentence_number, content = res.fetchone()
        return {'id': identifier,
                'document_id': document_id,
                'document': document,
                'sentence_number': sentence_number,
                'sentence_content': content,
                }

    def get_sentences_by_document_id(self, document_id: int) -> List[dict]:
        cur = self._con.cursor()
        res = cur.execute("SELECT id, sentence_number, content FROM sentence WHERE document_id = ? ORDER BY sentence_number", (document_id,))
        sentences = res.fetchall()
        result = [{'id': id,
                   'document_id': document_id,
                   'sentence_number': sentence_number,
                   'content': content
                  }
                 for id, sentence_number, content  in sentences]
        cur.close()
        return result