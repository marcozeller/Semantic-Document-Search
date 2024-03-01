from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from similarity_search import get_similar_sentences, get_documents_in_db, get_document_content_by_id
from os import path, getcwd, makedirs, listdir
from shutil import copyfileobj
from starlette.exceptions import HTTPException as StarletteHTTPException

# Some parameters which might be useful to change
# Directory where the documents are stored and loaded from for the search.
DOCUMENTS_DIRECTORY = path.join(getcwd(), "documents")

app = FastAPI()

# Allow local CORS.
# If you want external applications to use the API directly add them here.
origins = [
    "http://localhost.*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In case the user navigates to a non-existing page, redirect to the front-end.
class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try: 
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                #return await super().get_response('/', scope)
                return RedirectResponse(url='/ui')
            else:
                raise ex

app.mount("/ui", SPAStaticFiles(directory="front/build", html=True), name="ui")

@app.get("/")
async def front():
    return RedirectResponse(url='/ui')

@app.get("/api/document/{document_id}")
async def read_item(document_id: int):
    return get_document_content_by_id(document_id)

@app.get("/api/similar-sentences")
async def similar_sentences(number_results: int = 10, sentence: str = "No sentence provided"):
    return get_similar_sentences(sentence, number_results)

@app.post("/api/file")
async def create_upload_file(file: UploadFile):
    upload_dir = DOCUMENTS_DIRECTORY
    # Inspired by: https://www.slingacademy.com/article/fastapi-how-to-upload-and-validate-files/

    # check the content type (MIME type)
    content_type = file.content_type
    if content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Create the upload directory if it doesn't exist
    if not path.exists(upload_dir):
        makedirs(upload_dir)

    # get the destination path
    dest = path.join(upload_dir, file.filename)
    print(dest)

    # copy the file contents
    with open(dest, "wb") as buffer:
        copyfileobj(file.file, buffer)

    return {"filename": file.filename}

@app.get("/api/documents")
async def get_available_documents():
    documents_dir = DOCUMENTS_DIRECTORY
    stored_documents = listdir(documents_dir) # Get all files in the directory
    stored_documents = filter(lambda x: x.endswith(".pdf"), stored_documents) # Filter for PDFs
    stored_documents = map(lambda d: path.join(DOCUMENTS_DIRECTORY, d), stored_documents)
    stored_documents = list(stored_documents)

    documents_in_db = get_documents_in_db()
    paths_in_db = {d['path'] for d in documents_in_db}

    result = []

    for document_path in stored_documents:
        if document_path in paths_in_db:
            continue
        document_entry = {"identifier": None, "title": None, "path": document_path}
        result.append(document_entry)
    
    # Remove documents which are already in the database
    result = list(filter(lambda x: x["path"] not in documents_in_db, result))
    # Add the documents which are already in the database with their addtionial information
    result += documents_in_db
    
    return result

