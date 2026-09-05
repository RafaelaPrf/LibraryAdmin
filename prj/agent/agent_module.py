from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools import tool
import httpx

model = OllamaModel(model_id="qwen3:4b", host="http://localhost:11434")
TOOL_SERVER = "http://localhost:8090"

@tool
def get_books_by_author(author_name: str) -> dict:
    """Get all books by a specific author."""
    try:
        r = httpx.get(
            f"{TOOL_SERVER}/mcp/tools/books/by_author",
            params={"author": author_name},
            timeout=10.0
        )
        r.raise_for_status()
        data = r.json()
        if "result" in data:
            return {"results": data["result"], "error": None}
        else:
            return {"results": data, "error": None}
    except Exception as e:
        return {"results": None, "error": str(e)}

@tool
def get_books_by_rating(min_rating: int) -> dict:
    try:
        r = httpx.get(
            f"{TOOL_SERVER}/mcp/tools/books/by-rating",
            params={"min_rating": min_rating},
            timeout=10.0
        )
        r.raise_for_status()
        data = r.json()
        return {"results": data.get("result", []), "error": None}
    except Exception as e:
        return {"results": None, "error": str(e)}


agent = Agent(
    model=model,
    tools=[get_books_by_author,get_books_by_rating],
    system_prompt=(
        "You are a strict database assistant for a library system. "
        "You MUST use the available tools to answer ANY question about books, authors, or inventory. "
        "NEVER use your internal knowledge – if the tool returns no results, "
        "tell the user exactly that (e.g., 'No books found for this author'). "
        "Do not generate book titles or information from memory."
    )
)