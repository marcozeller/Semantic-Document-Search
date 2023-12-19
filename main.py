from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from random import random, randint

app = FastAPI()

app.mount("/ui", StaticFiles(directory="front/build", html=True), name="ui")

@app.get("/")
async def front():
    return RedirectResponse(url='ui')

@app.get("/api/item/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/api/similar-sentences")
async def similar_sentences(number_results: int = 10, sentence: str = "No sentence provided"):
    sentences = [sentence for _ in range(number_results)]
    similarity_scores = [random() for _ in range(number_results)]
    documents = ["document placeholder" for _ in range(number_results)]
    sentence_numbers = [randint(1, 1500) for _ in range(number_results)]

    result = [{"sentence_content": sentence,
               "similarity_score": similarity_score,
               "document": document,
               "document_id": 42,
               "sentence_number": sentence_number}
               for sentence, similarity_score, document, sentence_number
               in zip(sentences, similarity_scores, documents, sentence_numbers)]
    
    result.sort(key=lambda x: x["similarity_score"], reverse=True)

    return result

