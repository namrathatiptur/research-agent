"""Setup script for initializing the research agent."""
import os
import sqlite3
from pathlib import Path

def setup_directories():
    """Create necessary directories."""
    directories = [
        "data/chroma",
        "data",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"[OK] Created directory: {directory}")


def setup_database():
    """Initialize the SQLite database."""
    db_path = os.getenv("DATABASE_PATH", "./data/research.db")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a sample table for research notes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            note TEXT NOT NULL,
            source_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"[OK] Initialized database: {db_path}")


def check_env_file():
    """Check if .env file exists."""
    if not Path(".env").exists():
        print("[WARNING] .env file not found. Copy .env.example to .env and fill in your API keys.")
    else:
        print("[OK] .env file found")


def main():
    """Run setup."""
    print("Setting up Research Agent...")
    print()
    
    setup_directories()
    setup_database()
    check_env_file()
    
    print()
    print("Setup complete!")
    print()
    print("Next steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your API keys to .env")
    print("3. Run: streamlit run app/streamlit_app.py")


if __name__ == "__main__":
    main()

