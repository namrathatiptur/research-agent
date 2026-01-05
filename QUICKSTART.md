# Quick Start Guide

Get up and running with the Research Agent in minutes!

## Prerequisites

- Python 3.11 or higher
- API keys for:
  - Anthropic (Claude API)
  - Tavily (for web search)

## Installation Steps

1. **Install dependencies:**
```bash
pip install -e ".[dev]"
```

2. **Set up environment:**
```bash
cp .env.example .env
```

3. **Edit `.env` file and add your API keys:**
```env
ANTHROPIC_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

4. **Run setup script:**
```bash
python setup.py
```

5. **Start the Streamlit interface:**
```bash
streamlit run app/streamlit_app.py
```

6. **Or start the FastAPI backend:**
```bash
uvicorn app.api:app --reload
```

## First Research Query

Try asking:
- "What are the latest developments in quantum computing?"
- "Explain the benefits of renewable energy"
- "What is LangGraph and how does it work?"

## Troubleshooting

### Import Errors
Make sure you've installed the package:
```bash
pip install -e .
```

### API Key Errors
Verify your `.env` file has the correct keys and no extra spaces.

### ChromaDB Errors
Make sure the `data/chroma` directory exists:
```bash
mkdir -p data/chroma
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the test suite in `tests/`
- Explore the agent code in `src/agent/`

