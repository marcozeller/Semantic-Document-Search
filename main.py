from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from similarity_search import get_similar_sentences
from os import path, getcwd, makedirs
from shutil import copyfileobj

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

app.mount("/ui", StaticFiles(directory="front/build", html=True), name="ui")

@app.get("/")
async def front():
    return RedirectResponse(url='ui')

@app.get("/api/item/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/api/similar-sentences")
async def similar_sentences(number_results: int = 10, sentence: str = "No sentence provided"):
    return get_similar_sentences(sentence, number_results)

@app.post("/api/file")
async def create_upload_file(file: UploadFile):
    # Inspired by: https://www.slingacademy.com/article/fastapi-how-to-upload-and-validate-files/

    # check the content type (MIME type)
    content_type = file.content_type
    if content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    upload_dir = path.join(getcwd(), "documents")
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

