from langchain_groq import ChatGroq
from config.settings import GROQ_MODEL_NAME, DEFAULT_TEMPERATURE, set_api_key

class LLM:
    """
    LLM Manager for Groq models.

    Handles LLM initialization with configurable temperature.
    Temperature controls randomness in responses:
    - 0.0 = Deterministic, focused
    - 0.7 = Balanced (default)
    - 1.0 = Creative, diverse
    """

    def __init__(self, api_key: str = None, temperature: float = None):
        """
        Initialize the LLM.

        Args:
            api_key: Groq API key (optional, can use env var)
            temperature: Controls randomness (0.0-1.0). Defaults to config value.
        """
        if api_key:
            set_api_key(api_key)

        # Use provided temperature or default from config
        self.temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
        self.llm = ChatGroq(model=GROQ_MODEL_NAME, temperature=self.temperature)

    def get(self):
        """Get the LLM instance."""
        return self.llm

    def update_temperature(self, temperature: float):
        """
        Update the temperature and recreate the LLM.

        Args:
            temperature: New temperature value (0.0-1.0)
        """
        self.temperature = temperature
        self.llm = ChatGroq(model=GROQ_MODEL_NAME, temperature=self.temperature)

