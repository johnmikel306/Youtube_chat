import streamlit as st
from beyondllm.source import fit
from beyondllm.embeddings import HuggingFaceEmbeddings
from beyondllm.retrieve import auto_retriever
from beyondllm.llms import GroqModel
from beyondllm import generator
from beyondllm.memory import ChatBufferMemory
import os

# Streamlit config
st.set_page_config(page_title="BeyondLLM Demo", page_icon="🤖")

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Caching for expensive operations
@st.cache_data
def load_youtube_data(youtube_url):
    return fit(path=youtube_url, dtype="youtube")

@st.cache_resource
def get_embed_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def get_retriever(data, embed_model):
    return auto_retriever(data=data, embed_model=embed_model, type="normal", top_k=5)

@st.cache_resource
def get_llm():
    return GroqModel(model="llama3-8b-8192")

def main():
    st.title("BeyondLLM Demo")

    # YouTube URL input
    youtube_url = st.text_input("Enter the YouTube URL:", "https://www.youtube.com/watch?v=2CRKo4holSU")

    if youtube_url:
        # Load YouTube data
        with st.spinner("Loading YouTube data..."):
            data = load_youtube_data(youtube_url)
        st.success("YouTube data loaded successfully!")

        # Initialize components
        embed_model = get_embed_model()
        retriever = get_retriever(data, embed_model)
        
        # Check for GROQ API key in Streamlit secrets
        if 'GROQ_API_KEY' not in st.secrets:
            st.error("GROQ API key not found. Please add it to your Streamlit secrets.")
        else:
            os.environ['GROQ_API_KEY'] = st.secrets['GROQ_API_KEY']
            llm = get_llm()

            # User input
            user_prompt = st.text_input("Enter your question:")

            if user_prompt:
                with st.spinner("Generating response..."):
                    system_prompt = "You are an AI assistant that answers questions based on YouTube video content."
                    memory = ChatBufferMemory(window_size=5)  # Retains the last 5 interactions
                    
                    # Add current conversation to history
                    st.session_state.conversation_history.append(("User", user_prompt))
                    
                    # Generate response
                    pipeline = generator.Generate(question=user_prompt, system_prompt=system_prompt, llm=llm, retriever=retriever, memory=memory)
                    response = pipeline.call()
                    
                    # Add AI response to history
                    st.session_state.conversation_history.append(("AI", response))
                    
                    # Display response
                    st.write("AI Response:", response)

            # Display conversation history
            st.subheader("Conversation History")
            for role, message in st.session_state.conversation_history[-10:]:  # Show last 10 messages (5 conversations)
                st.text(f"{role}: {message}")

    else:
        st.warning("Please enter a YouTube URL to get started.")

if __name__ == "__main__":
    main()
