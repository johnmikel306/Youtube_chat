from beyondllm.source import fit
from beyondllm.embeddings import HuggingFaceEmbeddings
from beyondllm.retrieve import auto_retriever
from beyondllm.vectordb import ChromaVectorDb
from beyondllm.llms import GroqModel
from beyondllm import generator, retrieve
from beyondllm.memory import ChatBufferMemory
import streamlit as st
import os

# Initialize Streamlit app
st.title("YouTube QA-Bot")

# Upload YouTube URLs
youtube_urls = st.text_area("Enter YouTube URLs (comma-separated):")

if st.button("Process YouTube Data"):
    if youtube_urls:
        data = fit(path=youtube_urls.split(','), dtype="youtube")
        embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        text_embeddings = embed_model.embed_text("Huggingface models are awesome!")
        retriever = auto_retriever(data=data, embed_model=embed_model, type="normal", top_k=5)
        st.success("YouTube data processed successfully.")
    else:
        st.error("Please enter valid YouTube URLs.")

# Ask a question
user_prompt = st.text_input("Ask a question about the processed data:")

if st.button("Get Answer"):
    if user_prompt:
        os.environ['GROQ_API_KEY'] = st.secrets["GROQ_API_KEY"]
        llm = GroqModel(model="llama3-8b-8192")
        
        system_prompt = "You are an AI assistant...."
        pipeline = generator.Generate(question=user_prompt, system_prompt=system_prompt, llm=llm, retriever=retriever)
        
        response = pipeline.call()
        st.write("Response:", response)
    else:
        st.error("Please enter a question.")

# Memory management
if st.button("Initialize Memory"):
    memory = ChatBufferMemory(window_size=3)  # Retains the last three interactions
    st.success("Memory initialized.")
