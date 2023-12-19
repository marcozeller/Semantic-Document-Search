from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

app = FastAPI()

app.mount("/ui", StaticFiles(directory="front/build", html=True), name="ui")

@app.get("/")
async def front():
    return RedirectResponse(url='ui')

@app.get("/api/item/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

