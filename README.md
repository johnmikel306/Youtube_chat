# YouTube Video Analysis with LLM

Welcome to **YouTube Video Analysis with LLM**, an AI-powered application that extracts, processes, and analyzes content from YouTube videos. This project leverages state-of-the-art language models, embedding techniques, and retrieval systems to provide detailed insights into video content.

---

## Features

- **YouTube Data Processing**: Extracts video content and converts it into text for analysis.
- **Text Embedding**: Uses Hugging Face models for generating embeddings of text data.
- **Retriever System**: Automatically retrieves relevant information from processed data.
- **Large Language Model (LLM)**: Powered by GroqModel for intelligent, context-aware responses.
- **Interactive Interface**: Enables user-friendly interaction to query video content insights.
- **Memory Management**: Retains recent interactions for enhanced context in follow-up queries.

---

## Requirements

### API Key
The application requires a **GROQ API Key** for accessing the GroqModel LLM. Ensure you have the key available when running the app.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your GROQ API Key:
   - The app prompts you to enter your key during runtime.

4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## How It Works

1. **YouTube Data Loading**:
   - Enter a YouTube URL, and the app extracts video content using the `fit` function from the `beyondllm` library.

2. **Text Embedding**:
   - Embeds extracted text using `HuggingFaceEmbeddings` for advanced similarity search and retrieval.

3. **Retriever**:
   - Builds a retrieval system to fetch relevant information from the embedded data.

4. **Language Model Interaction**:
   - Integrates GroqModel for answering user queries based on retrieved content.

5. **User Interaction**:
   - Submit questions about the video content, and the AI provides comprehensive, contextually aware responses.

6. **Memory Retention**:
   - Maintains the last three user interactions to improve continuity in conversation.

---

## Usage

1. **Start the Application**:
   - Open the app in your browser after running the Streamlit command.

2. **Analyze Video**:
   - Enter a YouTube video URL to extract content for analysis.

3. **Ask Questions**:
   - Use the chat interface to ask questions about the video content.

4. **Follow-up Queries**:
   - Take advantage of memory retention for multi-turn conversations.

---

## Dependencies

- [Streamlit](https://streamlit.io/)
- [beyondllm](https://github.com/beyondllm)
- [Hugging Face Transformers](https://huggingface.co/)
- Python 3.8+

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests. For major changes, open a discussion to coordinate with the repository maintainers.

---

## License

This project is licensed under the MIT License.

---

Analyze YouTube videos like never before with cutting-edge AI! 🚀
