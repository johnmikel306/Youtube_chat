# 🎥 YouTube Video Q&A with LangGraph

A powerful, production-ready YouTube video question-answering system powered by LangGraph ReAct agents and Groq's Llama 3.3 70B model. Ask questions about any YouTube video and get accurate, context-aware answers based on the video's transcript.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/langchain-latest-green.svg)](https://langchain.com)
[![LangGraph](https://img.shields.io/badge/langgraph-latest-purple.svg)](https://langchain-ai.github.io/langgraph/)

## ✨ Features

- **🤖 LangGraph ReAct Agent**: Intelligent reasoning and action loop with forced tool usage for accurate answers
- **⚡ Groq Llama 3.3 70B**: Ultra-fast inference with excellent tool-calling capabilities
- **🔍 FAISS Vector Search**: Efficient semantic search over video transcripts
- **📺 YouTube Integration**: Robust transcript extraction using yt-dlp (bypasses IP blocking)
- **💬 Streaming Responses**: Real-time token-by-token response streaming
- **🌡️ Adjustable Temperature**: Control response creativity from UI, Studio, or CLI
- **🎨 Beautiful UI**: Clean, intuitive Streamlit interface with dark theme
- **🔧 LangGraph Studio Support**: Visual debugging and testing without UI
- **📝 Versioned Prompts**: File-based prompt management for easy experimentation
- **☁️ Cloud Ready**: Deploy instantly to Streamlit Cloud

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key (get one free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Youtube_chat
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**

   Create a `.env` file in the root directory:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

   Or export it directly:
   ```bash
   export GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser**

   Navigate to `http://localhost:8501`

## 📖 Usage

### Option 1: Web Interface (Streamlit)

1. **Enter your Groq API key** in the sidebar
2. **Adjust temperature** (0.0-1.0) to control response creativity
3. **Paste a YouTube URL** (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
4. **Click "Load Video"** to process the transcript
5. **Ask questions** about the video content in the chat interface
6. **Get streaming answers** powered by the ReAct agent

**Temperature Guide**:
- 🎯 **0.0** = Deterministic, focused (best for facts)
- ⚖️ **0.7** = Balanced (recommended default)
- 🎨 **1.0** = Creative, diverse (best for brainstorming)

### Option 2: LangGraph Studio (Visual Debugging)

Test and debug your agent visually without building a UI:

1. **Install LangGraph Studio** from [langchain-ai/langgraph-studio](https://github.com/langchain-ai/langgraph-studio)

2. **Open the project** in LangGraph Studio

3. **Fill in the required fields**:
   - **Messages**: Your question (e.g., "What is this video about?")
   - **Iterations**: `0`
   - **Video Url**: YouTube URL
   - **Video Loaded**: `false` (graph loads it automatically)
   - **Temperature**: `0.7`

4. **Click Submit** and watch the graph execute!

5. **View the response** in the **Chat** tab (easiest) or expand `messages` in the Output

**Features**:
- 📊 Visual graph representation with automatic video loading
- 🔍 Step-by-step debugging
- 👁️ State inspection at each node
- ⚡ Interactive testing
- 💬 Chat tab for easy response viewing

**Quick Guides**:
- [LangGraph Studio Guide](docs/LANGGRAPH_STUDIO_GUIDE.md) - Complete usage guide
- [Quick Start](docs/LANGGRAPH_STUDIO_QUICKSTART.md) - Get started in 2 minutes
- [Viewing Responses](docs/STUDIO_UI_GUIDE.md) - Where to find the agent's answers

**Or run the standalone CLI**:
```bash
python studio_graph.py
```

### Option 3: Programmatic Usage

```python
from src.app import YouTubeQA

# Initialize the system
qa = YouTubeQA(api_key="your_groq_api_key")

# Load a YouTube video
qa.load_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Ask a question (non-streaming)
answer = qa.ask("What is the main topic of this video?")
print(answer)

# Ask a question (streaming)
for chunk in qa.ask_stream("Summarize the key points"):
    print(chunk, end="", flush=True)
```

## 🏗️ Architecture

The system uses a modular architecture with clear separation of concerns:

```
Youtube_chat/
├── config/
│   └── settings.py              # Configuration and constants
├── prompts/
│   ├── system_prompt_v1.txt     # Versioned system prompts
│   ├── create_version.py        # Prompt versioning helper
│   └── README.md                # Prompt versioning guide
├── src/
│   ├── youtube_loader.py        # YouTube transcript extraction (yt-dlp)
│   ├── vector_store.py          # FAISS vector database
│   ├── llm_manager.py           # Groq LLM integration
│   ├── agent.py                 # LangGraph ReAct agent
│   └── app.py                   # Main application orchestration
├── docs/
│   ├── ARCHITECTURE.md          # System architecture details
│   ├── CODE_GUIDE.md            # Code walkthrough
│   ├── AGENT_FIXES.md           # Agent context usage fixes
│   ├── YT_DLP_MIGRATION.md      # yt-dlp migration guide
│   ├── TOOL_VALIDATION_FIX.md   # Tool validation error fix
│   ├── LANGGRAPH_STUDIO_GUIDE.md    # Complete Studio guide
│   ├── LANGGRAPH_STUDIO_QUICKSTART.md  # Quick start guide
│   ├── STUDIO_UI_GUIDE.md       # UI navigation guide
│   └── VIEWING_RESPONSES_IN_STUDIO.md  # Response viewing guide
├── tests/
│   ├── test_env.py              # Environment variable tests
│   ├── test_ytdlp.py            # yt-dlp loader tests
│   ├── test_studio.py           # Studio graph tests
│   └── test_temperature.py      # Temperature control tests
├── streamlit_app.py             # Streamlit web interface
├── studio_graph.py              # LangGraph Studio standalone graph
├── langgraph.json               # LangGraph Studio configuration
├── .env.example                 # Environment variables template
└── requirements.txt             # Python dependencies
```

### Key Components

- **YouTubeLoader**: Extracts and chunks video transcripts using yt-dlp (bypasses IP blocking)
- **VectorStore**: FAISS-based semantic search over transcript chunks
- **LLM**: Groq Llama 3.3 70B model wrapper with excellent tool-calling
- **Agent**: LangGraph ReAct agent with forced tool usage for context awareness
- **YouTubeQA**: Main application class orchestrating all components
- **Studio Graph**: Standalone graph with automatic video loading for LangGraph Studio

## ⚙️ Configuration

### Model & Agent Settings

Edit `config/settings.py` to customize:

```python
# Model Configuration
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"  # Groq model (excellent tool calling)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_TEMPERATURE = 0.7   # Default LLM temperature

# Vector DB Settings
CHUNK_SIZE = 1000           # Size of text chunks
CHUNK_OVERLAP = 200         # Overlap between chunks
TOP_K = 5                   # Number of chunks to retrieve

# Agent Settings
MAX_ITERATIONS = 10         # Maximum ReAct iterations

# Prompt Version
PROMPT_VERSION = "v1"       # Which prompt version to use
```

### Environment Variables

Create a `.env` file (see `.env.example`):

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (for LangSmith tracing)
LANGSMITH_API_KEY=your_langsmith_api_key_here
```

### Prompt Management

Prompts are versioned in the `prompts/` directory for easy experimentation:

```bash
prompts/
├── system_prompt_v1.txt    # Current active prompt
├── system_prompt_v2.txt    # Experimental version
└── README.md               # Versioning guide
```

**To create a new prompt version:**

1. Copy the current prompt:
   ```bash
   cp prompts/system_prompt_v1.txt prompts/system_prompt_v2.txt
   ```

2. Edit the new version with your changes

3. Update `config/settings.py`:
   ```python
   PROMPT_VERSION = "v2"
   ```

4. Test and compare results

See [prompts/README.md](prompts/README.md) for detailed prompt engineering guidelines.

## 🛠️ Technology Stack

| Component | Technology | Version/Details |
|-----------|-----------|-----------------|
| **LLM** | Groq Llama 3.3 70B | Versatile model with excellent tool calling |
| **Embeddings** | HuggingFace Sentence Transformers | all-MiniLM-L6-v2 |
| **Vector DB** | FAISS | CPU-optimized for fast similarity search |
| **Agent Framework** | LangGraph | ReAct pattern with forced tool usage |
| **LLM Framework** | LangChain | Core + Community + Groq integration |
| **UI** | Streamlit | Dark theme, streaming responses |
| **Transcript Extraction** | yt-dlp | Robust, bypasses YouTube IP blocking |
| **Development Tools** | LangGraph Studio | Visual debugging and testing |


## 🌐 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add your `GROQ_API_KEY` in the Secrets section:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
5. Deploy!

### Local Production

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production settings
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 🔧 Troubleshooting

### Common Issues

**"No API key found" / "GROQ_API_KEY not set"**
- Make sure you've created a `.env` file with `GROQ_API_KEY=your_key`
- Or enter it directly in the Streamlit sidebar
- Check that `.env` is in the project root directory
- Restart the application after adding the key

**"Failed to load video" / "Could not retrieve transcript"**
- Ensure the YouTube URL is valid
- Check that the video has English captions/transcripts available
- **IP Blocking**: We use yt-dlp which bypasses most IP blocks
- Try a different video to verify the system works
- Check your internet connection

**"Tool validation failed" (LangGraph Studio)**
- This has been fixed in the latest version
- Make sure you're using the updated `studio_graph.py`
- Restart LangGraph Studio to pick up code changes

**"Can't see agent response" (LangGraph Studio)**
- Click the **Chat** tab at the top to see formatted responses
- Or expand the `messages` array in Output and look at the last AI message
- See [Viewing Responses Guide](docs/VIEWING_RESPONSES_IN_STUDIO.md)

**"System not ready"**
- Make sure you've loaded a video before asking questions
- Check that the API key is valid
- In LangGraph Studio, set `video_loaded: false` - the graph loads it automatically

**Slow responses**
- The first query may be slower due to model initialization
- Video loading can take 10-30 seconds depending on video length
- Subsequent queries should be much faster with Groq's inference
- yt-dlp caches data, so re-loading the same video is faster

**Agent not using video context**
- This has been fixed with forced tool usage
- The agent now ALWAYS searches the video on the first question
- System prompt enforces context-based answers
- See [Agent Fixes Documentation](docs/AGENT_FIXES.md)

## 📝 Example Questions

Try asking questions like:

- "What is the main topic of this video?"
- "Summarize the key points discussed"
- "What examples are mentioned?"
- "Who is the speaker talking about?"
- "What are the conclusions?"
- "Explain the concept discussed at [timestamp]"
- "What are the three main arguments?"
- "How does the speaker explain [topic]?"

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

### Getting Started
- [Architecture Overview](docs/ARCHITECTURE.md) - System design and components
- [Code Guide](docs/CODE_GUIDE.md) - Detailed code walkthrough

### LangGraph Studio
- [Complete Studio Guide](docs/LANGGRAPH_STUDIO_GUIDE.md) - Full usage instructions
- [Quick Start](docs/LANGGRAPH_STUDIO_QUICKSTART.md) - Get started in 2 minutes
- [UI Navigation](docs/STUDIO_UI_GUIDE.md) - Where to find everything
- [Viewing Responses](docs/VIEWING_RESPONSES_IN_STUDIO.md) - How to see agent answers

### Technical Details
- [Agent Context Fixes](docs/AGENT_FIXES.md) - How we fixed context awareness
- [yt-dlp Migration](docs/YT_DLP_MIGRATION.md) - Why and how we switched from youtube-transcript-api
- [Tool Validation Fix](docs/TOOL_VALIDATION_FIX.md) - Fixing LangGraph tool errors

### Prompt Engineering
- [Prompt Versioning](prompts/README.md) - How to create and test new prompts

## 🧪 Testing

The project includes several test scripts in the `tests/` directory:

### Test Environment Setup
```bash
python tests/test_env.py
```
Verifies that `.env` file is loaded correctly and API key is accessible.

### Test yt-dlp Loader
```bash
python tests/test_ytdlp.py
```
Tests YouTube transcript extraction with yt-dlp.

### Test Studio Graph
```bash
python tests/test_studio.py
```
Tests the LangGraph Studio graph imports and builds correctly.

### Test Temperature Control
```bash
python tests/test_temperature.py
```
Verifies temperature parameter works across all components.

### Run All Tests
```bash
# Run all test files
for test in tests/test_*.py; do python "$test"; done
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions and classes
- Include comments for complex logic
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License.

## 🎯 Recent Improvements

### v2.0 (Current)
- ✅ **Migrated to yt-dlp** - Bypasses YouTube IP blocking, more reliable transcript extraction
- ✅ **Upgraded to Llama 3.3 70B** - Better tool calling and instruction following
- ✅ **Forced tool usage** - Agent always searches video context before answering
- ✅ **Strengthened prompts** - Prevents hallucination and generic answers
- ✅ **Fixed tool validation** - Singleton pattern for consistent tool instances
- ✅ **Automatic video loading** - LangGraph Studio loads videos automatically
- ✅ **Comprehensive documentation** - 8+ detailed guides in docs/ folder
- ✅ **Better error handling** - Clear, actionable error messages
- ✅ **Environment variable fixes** - Proper .env loading on all platforms
- ✅ **Windows UTF-8 support** - Emoji and special characters work correctly

### v1.0
- Initial release with GPT-OSS 20B
- Basic ReAct agent implementation
- Streamlit UI with streaming
- youtube-transcript-api integration

## 🙏 Acknowledgments

- [Groq](https://groq.com) for ultra-fast LLM inference with Llama 3.3 70B
- [LangChain](https://langchain.com) & [LangGraph](https://langchain-ai.github.io/langgraph/) for the agent framework
- [Streamlit](https://streamlit.io) for the amazing UI framework
- [FAISS](https://github.com/facebookresearch/faiss) for efficient vector search
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for robust YouTube transcript extraction
- [HuggingFace](https://huggingface.co) for sentence transformers

## 📧 Support

For issues and questions, please open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Multi-language support (non-English videos)
- [ ] Video timestamp linking in responses
- [ ] Conversation memory across sessions
- [ ] Batch video processing
- [ ] Export conversation history
- [ ] Custom embedding models
- [ ] Proxy support for restricted networks

---

**Built with ❤️ using LangGraph, Groq, and yt-dlp**

