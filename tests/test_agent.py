"""Tests for the research agent."""
import pytest
from src.agent.graph import run_research
from src.agent.state import ResearchState


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires API keys and may be slow")
async def test_simple_research():
    """Test a simple research query."""
    result = await run_research("What is the capital of France?")
    
    assert result is not None
    assert isinstance(result, dict)
    assert "query" in result
    assert result["query"] == "What is the capital of France?"


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires API keys and may be slow")
async def test_research_with_memory():
    """Test research that should use memory."""
    # First query
    result1 = await run_research("What is Python programming?")
    assert result1 is not None
    
    # Second query that should benefit from memory
    result2 = await run_research("Tell me more about Python")
    assert result2 is not None

