"""
Brainstorming the interfaces in the project

What needs to be standardized:
- Documents single class interface around multiple types of documents
    - pdf,
    - docx,
    - txt,
    - html

Formats:
- python natives (lists, dicts, and primitive types) -> avoid as no guarantees
- pandas dataframes while batch processing -> check before and after for schema
- dataclasses ?
- pydantic ?
- SQLAlchemy
"""
from pydantic import BaseModel
import pandera as pa
from pandera.engines.pandas_engine import PydanticModel

# Define the interfaces as Pydantic models which can be validated and serialized
class Sentence(BaseModel):
    id: int
    document_id: int
    sentence_number: int
    content: str

class SimilarSentence(Sentence):
    document_title: str
    distance: float

class Document(BaseModel):
    id: int|None
    title: str|None
    path: str

# When comming from the database further restrictions can be added
# When storing in the database these models must be used to validate the data
class DBDocument(Document):
    id: int
    title: str

# For operations on batch data, we can use Pandera DataFrameModel derived from the Pydantic models
class Sentences(pa.DataFrameModel):
    class Config:
        dtype = PydanticModel(Sentence)
        coerce = True

class SimilarSentences(pa.DataFrameModel):
    class Config:
        dtype = PydanticModel(SimilarSentence)
        coerce = True

class Documents(pa.DataFrameModel):
    class Config:
        dtype = PydanticModel(Document)
        coerce = True