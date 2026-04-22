import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_web(query: str) -> str:
    """Search the web for recent articles, research papers, or any study topic.
    Use this when the user asks about current events or recent research."""
    response = client.search(query=query, max_results=5)
    results = response.get("results", [])
    if not results:
        return "No results found for that query."
    return "\n\n".join([
        f"Title: {r['title']}\nURL: {r['url']}\nSummary: {r['content'][:300]}"
        for r in results
    ])