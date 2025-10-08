# 🎥 YouTube Video Q&A with LangGraph

A powerful, minimal YouTube video question-answering system powered by LangGraph ReAct agents and Groq's GPT-OSS model. Ask questions about any YouTube video and get accurate, context-aware answers based on the video's transcript.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/langchain-latest-green.svg)](https://langchain.com)

## ✨ Features

- **🤖 LangGraph ReAct Agent**: Intelligent reasoning and action loop for accurate answers
- **⚡ Groq GPT-OSS**: Ultra-fast inference with OpenAI's GPT-OSS 20B model
- **🔍 FAISS Vector Search**: Efficient semantic search over video transcripts
- **📺 YouTube Integration**: Automatic transcript extraction from any YouTube video
- **💬 Streaming Responses**: Real-time token-by-token response streaming
- **🌡️ Adjustable Temperature**: Control response creativity from UI or Studio
- **🎨 Beautiful UI**: Clean, intuitive Streamlit interface
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

```bash
# Run the standalone graph
python studio_graph.py
```

Or open the project in [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) for:
- 📊 Visual graph representation
- 🔍 Step-by-step debugging
- 👁️ State inspection at each node
- ⚡ Interactive testing

See [LangGraph Studio Guide](docs/LANGGRAPH_STUDIO_GUIDE.md) for detailed instructions.

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
│   └── settings.py          # Configuration and constants
├── prompts/
│   ├── system_prompt_v1.txt # Versioned system prompts
│   └── README.md            # Prompt versioning guide
├── src/
│   ├── youtube_loader.py    # YouTube transcript extraction
│   ├── vector_store.py      # FAISS vector database
│   ├── llm_manager.py       # Groq LLM integration
│   ├── agent.py             # LangGraph ReAct agent
│   └── app.py               # Main application orchestration
├── streamlit_app.py         # Streamlit web interface
├── studio_graph.py          # LangGraph Studio standalone graph
├── langgraph.json           # LangGraph Studio configuration
└── requirements.txt         # Python dependencies
```

### Key Components

- **YouTubeLoader**: Extracts and chunks video transcripts
- **VectorStore**: FAISS-based semantic search over transcript chunks
- **LLM**: Groq GPT-OSS 20B model wrapper
- **Agent**: LangGraph ReAct agent with tool-calling capabilities
- **YouTubeQA**: Main application class orchestrating all components

## ⚙️ Configuration

### Model & Agent Settings

Edit `config/settings.py` to customize:

```python
# Model Configuration
GROQ_MODEL_NAME = "openai/gpt-oss-20b"  # Groq model to use
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Vector DB Settings
CHUNK_SIZE = 1000           # Size of text chunks
CHUNK_OVERLAP = 200         # Overlap between chunks
TOP_K = 5                   # Number of chunks to retrieve

# Agent Settings
MAX_ITERATIONS = 10         # Maximum ReAct iterations

# Prompt Version
PROMPT_VERSION = "v1"       # Which prompt version to use
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

| Component | Technology |
|-----------|-----------|
| **LLM** | Groq GPT-OSS 20B |
| **Embeddings** | HuggingFace Sentence Transformers |
| **Vector DB** | FAISS |
| **Agent Framework** | LangGraph |
| **LLM Framework** | LangChain |
| **UI** | Streamlit |
| **Transcript API** | youtube-transcript-api |


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

**"No API key found"**
- Make sure you've set the `GROQ_API_KEY` environment variable
- Or enter it directly in the Streamlit sidebar

**"Failed to load video"**
- Ensure the YouTube URL is valid
- Check that the video has captions/transcripts available
- Some videos may have transcripts disabled

**"System not ready"**
- Make sure you've loaded a video before asking questions
- Check that the API key is valid

**Slow responses**
- The first query may be slower due to model initialization
- Subsequent queries should be much faster with Groq's inference

## 📝 Example Questions

Try asking questions like:

- "What is the main topic of this video?"
- "Summarize the key points discussed"
- "What examples are mentioned?"
- "Who is the speaker talking about?"
- "What are the conclusions?"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for ultra-fast LLM inference
- [LangChain](https://langchain.com) for the LLM framework
- [Streamlit](https://streamlit.io) for the amazing UI framework
- [FAISS](https://github.com/facebookresearch/faiss) for efficient vector search

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using LangGraph and Groq**

