"""Tool registry and management for MCP tools."""
import os
from typing import Any, Dict, List

from langchain_core.tools import Tool as LangChainTool
from langchain_anthropic import ChatAnthropic


def create_web_search_tool() -> LangChainTool:
    """Create a LangChain tool wrapper for web search."""
    from tavily import TavilyClient

    def search_web(query: str, max_results: int = 5) -> str:
        """Search the web using Tavily."""
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY not set"

        client = TavilyClient(api_key=api_key)
        try:
            results = client.search(query=query, max_results=max_results)
            formatted = []
            for r in results.get("results", []):
                formatted.append(
                    f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r.get('content', '')}"
                )
            return "\n---\n".join(formatted) if formatted else "No results found"
        except Exception as e:
            return f"Error: {str(e)}"

    return LangChainTool(
        name="web_search",
        description="Search the web for current information on any topic",
        func=search_web
    )


def create_memory_tools() -> List[LangChainTool]:
    """Create LangChain tool wrappers for memory operations."""
    import chromadb
    from chromadb.config import Settings
    from datetime import datetime

    chroma_path = os.getenv("CHROMA_PATH", "./data/chroma")
    os.makedirs(chroma_path, exist_ok=True)

    client = chromadb.PersistentClient(
        path=chroma_path,
        settings=Settings(anonymized_telemetry=False)
    )
    collection = client.get_or_create_collection(
        name="agent_memory",
        metadata={"hnsw:space": "cosine"}
    )

    def store_memory(content: str, metadata: str = "{}") -> str:
        """Store information in memory."""
        try:
            import json
            meta = json.loads(metadata) if metadata else {}
            doc_id = f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            meta["timestamp"] = datetime.now().isoformat()
            collection.add(documents=[content], ids=[doc_id], metadatas=[meta])
            return f"Memory stored with ID: {doc_id}"
        except Exception as e:
            return f"Error: {str(e)}"

    def search_memory(query: str, n_results: int = 5) -> str:
        """Search stored memories."""
        try:
            results = collection.query(query_texts=[query], n_results=n_results)
            memories = []
            if results.get("documents") and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    memories.append({
                        "content": doc,
                        "metadata": (
                            results["metadatas"][0][i]
                            if results.get("metadatas") and results["metadatas"][0]
                            else {}
                        )
                    })
            return str(memories) if memories else "No memories found"
        except Exception as e:
            return f"Error: {str(e)}"

    return [
        LangChainTool(
            name="store_memory",
            description="Store information in long-term memory",
            func=store_memory
        ),
        LangChainTool(
            name="search_memory",
            description="Search stored memories using semantic similarity",
            func=search_memory
        )
    ]


def get_all_tools() -> List[LangChainTool]:
    """Get all available tools."""
    tools = [create_web_search_tool()]
    tools.extend(create_memory_tools())
    return tools

