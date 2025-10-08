from src.youtube_loader import YouTubeLoader
from src.vector_store import VectorStore
from src.llm_manager import LLM
from src.agent import Agent

class YouTubeQA:
    """
    Main application class for YouTube Q&A.

    Orchestrates all components: video loading, vector store, LLM, and agent.
    Supports configurable temperature for controlling response randomness.
    """

    def __init__(self, api_key: str = None, temperature: float = None):
        """
        Initialize the YouTube Q&A system.

        Args:
            api_key: Groq API key (optional, can use env var)
            temperature: LLM temperature (0.0-1.0). Controls randomness.
        """
        self.loader = YouTubeLoader()
        self.vector_store = VectorStore()
        self.llm = LLM(api_key, temperature) if api_key else None
        self.temperature = temperature
        self.agent = None
        self.ready = False

    def set_api_key(self, api_key: str, temperature: float = None):
        """
        Set or update the API key and optionally temperature.

        Args:
            api_key: Groq API key
            temperature: Optional temperature override
        """
        temp = temperature if temperature is not None else self.temperature
        self.llm = LLM(api_key, temp)
        self.temperature = temp
        if self.vector_store.store:
            self._init_agent()

    def set_temperature(self, temperature: float):
        """
        Update the temperature setting.

        Args:
            temperature: New temperature value (0.0-1.0)
                        0.0 = Deterministic, focused
                        0.7 = Balanced (default)
                        1.0 = Creative, diverse
        """
        if not self.llm:
            raise ValueError("LLM not initialized. Set API key first.")

        self.temperature = temperature
        self.llm.update_temperature(temperature)

        # Reinitialize agent with updated LLM
        if self.vector_store.store:
            self._init_agent()

    def load_video(self, url: str) -> bool:
        """
        Load a YouTube video and create vector store.

        Args:
            url: YouTube video URL

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            docs = self.loader.load(url)
            self.vector_store.create(docs)
            if self.llm:
                self._init_agent()
            self.ready = self.agent is not None
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def _init_agent(self):
        """Initialize the agent with current LLM and vector store."""
        self.agent = Agent(self.llm.get(), self.vector_store.as_retriever())
        self.ready = True

    def ask(self, question: str) -> str:
        """
        Ask a question about the video (non-streaming).

        Args:
            question: Question to ask

        Returns:
            str: Answer from the agent
        """
        if not self.ready:
            raise ValueError("System not ready")
        return self.agent.run(question)

    def ask_stream(self, question: str):
        """
        Ask a question about the video (streaming).

        Args:
            question: Question to ask

        Yields:
            str: Answer chunks as they're generated
        """
        if not self.ready:
            raise ValueError("System not ready")
        for chunk in self.agent.stream(question):
            yield chunk

