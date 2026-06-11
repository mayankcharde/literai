from tavily import TavilyClient
import os
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def advanced_search(query: str, search_depth: str = "advanced", max_results: int = 5) -> Dict[str, Any]:
    """Advanced search with comprehensive results"""
    try:
        response = tavily.search(
            query=query,
            search_depth=search_depth,
            max_results=max_results,
            include_answer=True,
            include_raw_content=True,
            include_images=True
        )
        
        return {
            "query": query,
            "answer": response.get("answer", ""),
            "results": [
                {
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "url": r.get("url", ""),
                    "score": r.get("score", 0),
                    "raw_content": r.get("raw_content", "")
                }
                for r in response.get("results", [])
            ],
            "images": response.get("images", [])[:3]
        }
    except Exception as e:
        return {"query": query, "error": str(e), "results": []}

async def parallel_search(queries: List[str], max_concurrent: int = 3) -> List[Dict[str, Any]]:
    """Execute multiple searches in parallel"""
    results = []
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, advanced_search, q) for q in queries]
        results = await asyncio.gather(*tasks)
    return results

def search_with_followup(initial_query: str, followup_queries: List[str]) -> List[Dict[str, Any]]:
    """Search with follow-up questions"""
    all_results = [advanced_search(initial_query)]
    for fq in followup_queries[:3]:
        all_results.append(advanced_search(fq))
    return all_results