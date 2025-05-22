import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes import auth, books, readers, borrow

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrow.router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")

if os.path.isdir(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/docs/manual", response_class=HTMLResponse)
async def manual_docs():
    with open("app/static/docs/manual.html", "r", encoding="utf-8") as f:
        return f.read()