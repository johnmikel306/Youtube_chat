import os
from pathlib import Path

# Model Configuration
GROQ_MODEL_NAME = "openai/gpt-oss-20b"  # GPT-OSS 20B model from Groq
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# LLM Parameters
# Temperature controls randomness in responses (0.0 = deterministic, 1.0 = creative)
DEFAULT_TEMPERATURE = 0.7

# Vector DB
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5

# Agent
MAX_ITERATIONS = 10

# Prompt Configuration
# Change this to switch between prompt versions (e.g., "v1", "v2", "v3")
PROMPT_VERSION = "v1"

# Load system prompt from versioned file
def load_system_prompt(version: str = PROMPT_VERSION) -> str:
    """
    Load the system prompt from the prompts directory.

    This allows for easy prompt versioning and experimentation.
    To create a new version:
    1. Copy prompts/system_prompt_v1.txt to prompts/system_prompt_v2.txt
    2. Edit the new file
    3. Change PROMPT_VERSION = "v2" above

    Args:
        version: The prompt version to load (e.g., "v1", "v2")

    Returns:
        str: The system prompt text
    """
    # Get the project root directory (parent of config/)
    project_root = Path(__file__).parent.parent
    prompt_file = project_root / "prompts" / f"system_prompt_{version}.txt"

    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback to default prompt if file not found
        print(f"Warning: Prompt file {prompt_file} not found. Using default prompt.")
        return """You are an AI assistant that answers questions about YouTube videos.
Use the search tool to find relevant information from the video transcript.
Provide clear, accurate answers based only on the video content."""

# Load the system prompt
SYSTEM_PROMPT = load_system_prompt()

def get_api_key():
    """Get the Groq API key from environment variables."""
    return os.getenv("GROQ_API_KEY", "")

def set_api_key(key):
    """Set the Groq API key in environment variables."""
    os.environ["GROQ_API_KEY"] = key

