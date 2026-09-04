from fastapi import FastAPI

import httpx
from settings import get_default_api_base_url

app = FastAPI()

@app.get("/mcp/tools/books/by_author")
def get_books_by_author(author: str):
    try:
        main_api_url = get_default_api_base_url() + f"/books/by_author/{author}"
        r = httpx.get(main_api_url, timeout=10.0)
        r.raise_for_status()
        return {"result": r.json(), "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}

@app.get("/mcp/tools/books/by-rating")
def get_books_by_rating(min_rating: int):
    try:
        main_api_url = get_default_api_base_url() + f"/books/by-rating/{min_rating}"
        r = httpx.get(main_api_url, timeout=10.0)
        r.raise_for_status()
        return {"result": r.json(), "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}