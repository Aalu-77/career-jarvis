import os
from pathlib import Path
from dotenv import load_dotenv

# Find the project root (the folder containing this src/ folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from .env file in project root
load_dotenv(PROJECT_ROOT / ".env")

# Fail loudly if the API key is missing — better than a confusing error later
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError(
        "ANTHROPIC_API_KEY not found. "
        "Make sure you have a .env file in the project root with this line:\n"
        "ANTHROPIC_API_KEY=sk-ant-..."
    )

# Paths
CV_PATH = PROJECT_ROOT / "config" / "cv.md"

# Models — Haiku is fast and cheap for screening, Sonnet for important work
MODEL_FAST = "claude-haiku-4-5-20251001"
MODEL_SMART = "claude-sonnet-4-5"

def load_cv() -> str:
    """Read the CV from config/cv.md."""
    if not CV_PATH.exists():
        raise FileNotFoundError(
            f"CV file not found at {CV_PATH}. "
            f"Create config/cv.md with your CV in markdown format."
        )
    return CV_PATH.read_text(encoding="utf-8")
