import streamlit as st
from beyondllm.source import fit
from beyondllm.embeddings import HuggingFaceEmbeddings
from beyondllm.retrieve import auto_retriever
from beyondllm.vectordb import ChromaVectorDb
from beyondllm.llms import GroqModel
from beyondllm import generator, retrieve
from beyondllm.memory import ChatBufferMemory
import os

def load_youtube_data(url):
    return fit(path=url, dtype="youtube")

def create_embeddings(model_name, text):
    embed_model = HuggingFaceEmbeddings(model_name=model_name)
    return embed_model.embed_text(text)

def setup_retriever(data, embed_model, top_k):
    return auto_retriever(data=data, embed_model=embed_model, type="normal", top_k=top_k)

def initialize_llm(api_key, model_name):
    os.environ['GROQ_API_KEY'] = api_key
    return GroqModel(model=model_name)

def generate_response(user_prompt, system_prompt, llm, retriever):
    pipeline = generator.Generate(question=user_prompt, system_prompt=system_prompt, llm=llm, retriever=retriever)
    return pipeline.call()

def main():
    st.title("YouTube Video Analysis with LLM")

    # Load YouTube data
    youtube_urls = st.text_input("Enter the YouTube URL:")
    if youtube_urls:
        data = load_youtube_data(youtube_urls)

        # Embedding
        text_embeddings = create_embeddings("sentence-transformers/all-MiniLM-L6-v2", "Huggingface models are awesome!")

        # Auto Retriever
        retriever = setup_retriever(data, text_embeddings, top_k=5)
        retrieved_nodes = retriever.retrieve("What is this video about?")

        # Initialize LLM with API key
        api_key = st.text_input("Enter your GROQ API Key:", type="password")
        if api_key:
            llm = initialize_llm(api_key, "llama3-8b-8192")

            # Generator
            user_prompt = st.text_input("Enter your question:")
            system_prompt = "You are an AI assistant...."
            if user_prompt:
                response = generate_response(user_prompt, system_prompt, llm, retriever)
                st.write(response)

            # Memory
            memory = ChatBufferMemory(window_size=3)  # Retains the last three interactions

if __name__ == "__main__":
    main()
