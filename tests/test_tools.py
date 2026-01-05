"""Tests for tool registry."""
import pytest
from src.tools.tool_registry import get_all_tools


def test_get_all_tools():
    """Test that tools can be retrieved."""
    tools = get_all_tools()
    assert len(tools) > 0
    
    # Check that expected tools are present
    tool_names = [t.name for t in tools]
    assert "web_search" in tool_names
    assert "store_memory" in tool_names
    assert "search_memory" in tool_names

