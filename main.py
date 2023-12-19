from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from similarity_search import get_similar_sentences
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
    return get_similar_sentences(sentence, number_results)

