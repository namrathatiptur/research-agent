"""
MCP Server for persistent memory using ChromaDB.

Tools:
- store_memory: Save information for later retrieval
- search_memory: Semantic search over stored memories
- clear_memory: Clear all stored memories
"""
import asyncio
import json
import os
from datetime import datetime
from typing import Any

import chromadb
from chromadb.config import Settings
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("memory-server")

# Initialize ChromaDB
chroma_path = os.getenv("CHROMA_PATH", "./data/chroma")
os.makedirs(chroma_path, exist_ok=True)

chroma_client = chromadb.PersistentClient(
    path=chroma_path,
    settings=Settings(anonymized_telemetry=False)
)
collection = chroma_client.get_or_create_collection(
    name="agent_memory",
    metadata={"hnsw:space": "cosine"}
)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="store_memory",
            description=(
                "Store a piece of information in long-term memory "
                "for later retrieval"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The information to remember"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata (source, topic, etc.)",
                        "default": {}
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="search_memory",
            description="Search through stored memories using semantic similarity",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="clear_memory",
            description="Clear all stored memories (use with caution)",
            inputSchema={"type": "object", "properties": {}}
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    if name == "store_memory":
        content = arguments.get("content", "")
        doc_id = f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        metadata = arguments.get("metadata", {})
        metadata["timestamp"] = datetime.now().isoformat()

        try:
            collection.add(
                documents=[content],
                ids=[doc_id],
                metadatas=[metadata]
            )

            return [TextContent(
                type="text",
                text=f"Memory stored with ID: {doc_id}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error storing memory: {str(e)}"
            )]

    elif name == "search_memory":
        query = arguments.get("query", "")
        n_results = arguments.get("n_results", 5)

        try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )

            memories = []
            if results.get("documents") and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    memory_item = {
                        "content": doc,
                        "metadata": (
                            results["metadatas"][0][i]
                            if results.get("metadatas") and results["metadatas"][0]
                            else {}
                        )
                    }
                    if results.get("distances") and results["distances"][0]:
                        memory_item["relevance"] = 1 - results["distances"][0][i]
                    memories.append(memory_item)

            if not memories:
                return [TextContent(
                    type="text",
                    text="No memories found matching the query"
                )]

            return [TextContent(
                type="text",
                text=json.dumps(memories, indent=2)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error searching memory: {str(e)}"
            )]

    elif name == "clear_memory":
        try:
            # Get all IDs and delete
            all_data = collection.get()
            all_ids = all_data.get("ids", [])
            if all_ids:
                collection.delete(ids=all_ids)
            return [TextContent(
                type="text",
                text=f"Cleared {len(all_ids)} memories"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error clearing memory: {str(e)}"
            )]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())

