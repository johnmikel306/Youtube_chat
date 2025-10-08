import streamlit as st
from src.app import YouTubeQA
import time

# ChatGPT-like page configuration
st.set_page_config(
    page_title="YouTube Q&A Chat",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsible sidebar like ChatGPT
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    /* Main chat container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 48rem;
        margin: 0 auto;
    }

    /* Chat input at bottom */
    .stChatFloatingInputContainer {
        bottom: 20px;
        background-color: transparent;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f7f7f8;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }

    /* Loading animation */
    .stSpinner > div {
        border-color: #10a37f !important;
    }

    /* Title styling */
    h1 {
        text-align: center;
        color: #202123;
        font-weight: 600;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'qa' not in st.session_state:
    st.session_state.qa = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'ready' not in st.session_state:
    st.session_state.ready = False
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7  # Default temperature
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'video_url' not in st.session_state:
    st.session_state.video_url = ""

# Collapsible Sidebar (ChatGPT-style)
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    # API Key Section
    st.markdown("#### 🔑 API Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API key...",
        help="Get your API key from https://console.groq.com"
    )

    if st.button("💾 Save API Key", use_container_width=True):
        if api_key:
            with st.spinner("Initializing..."):
                st.session_state.qa = YouTubeQA(api_key, st.session_state.temperature)
                st.success("✅ API key saved!")
                time.sleep(0.5)
        else:
            st.error("Please enter an API key")

    st.divider()

    # Video Loading Section
    st.markdown("#### 🎥 Video Source")
    video_url = st.text_input(
        "YouTube URL",
        value=st.session_state.video_url,
        placeholder="https://youtube.com/watch?v=...",
        help="Paste a YouTube video URL to analyze"
    )

    if st.button("📥 Load Video", use_container_width=True):
        if not st.session_state.qa:
            st.error("⚠️ Please set your API key first!")
        elif not video_url:
            st.error("⚠️ Please enter a YouTube URL!")
        else:
            with st.spinner("🔄 Loading and processing video transcript..."):
                try:
                    st.session_state.processing = True
                    if st.session_state.qa.load_video(video_url):
                        st.session_state.ready = True
                        st.session_state.video_url = video_url
                        st.success("✅ Video loaded successfully!")
                        time.sleep(0.5)
                    else:
                        st.error("❌ Failed to load video. Please check the URL.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                finally:
                    st.session_state.processing = False

    # Show loaded video info
    if st.session_state.ready and st.session_state.video_url:
        st.info(f"📺 Video loaded and ready!")

    st.divider()

    # Temperature Control
    st.markdown("#### 🌡️ Model Settings")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
        help="Lower = more focused, Higher = more creative"
    )

    # Update temperature if changed
    if temperature != st.session_state.temperature:
        st.session_state.temperature = temperature
        if st.session_state.qa:
            try:
                st.session_state.qa.set_temperature(temperature)
                st.success(f"✅ Temperature: {temperature}")
                time.sleep(0.3)
            except Exception as e:
                st.error(f"Error: {e}")

    # Temperature guide
    with st.expander("ℹ️ Temperature Guide"):
        st.markdown("""
        - **0.0-0.3**: Precise, factual
        - **0.4-0.7**: Balanced (recommended)
        - **0.8-1.0**: Creative, varied
        """)

    st.divider()

    # Chat controls
    st.markdown("#### 💬 Chat Controls")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat cleared!")
        time.sleep(0.3)
        st.rerun()

    # Stats
    if st.session_state.messages:
        msg_count = len(st.session_state.messages)
        st.caption(f"💬 {msg_count} message{'s' if msg_count != 1 else ''} in chat")

# Main chat interface - ChatGPT style
st.title("💬 YouTube Video Q&A")

# Welcome message or chat interface
if not st.session_state.ready:
    # Welcome screen (ChatGPT-like)
    st.markdown("""
    <div style='text-align: center; padding: 3rem 1rem;'>
        <h2 style='color: #10a37f; margin-bottom: 1rem;'>Welcome to YouTube Video Q&A</h2>
        <p style='font-size: 1.1rem; color: #6e6e80; margin-bottom: 2rem;'>
            Ask questions about any YouTube video using AI
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Getting started steps
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🔑</div>
            <h4>1. Set API Key</h4>
            <p style='color: #6e6e80; font-size: 0.9rem;'>Enter your Groq API key in the sidebar</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎥</div>
            <h4>2. Load Video</h4>
            <p style='color: #6e6e80; font-size: 0.9rem;'>Paste a YouTube URL and click Load</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>💬</div>
            <h4>3. Start Chatting</h4>
            <p style='color: #6e6e80; font-size: 0.9rem;'>Ask questions about the video content</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("👈 Open the sidebar to get started!", icon="ℹ️")

else:
    # Chat interface (ChatGPT-like)
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    # Chat input at bottom (ChatGPT-style)
    if prompt := st.chat_input("Ask me anything about the video...", key="chat_input"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        # Generate assistant response with loading animation
        with st.chat_message("assistant", avatar="🤖"):
            try:
                # Show loading indicator
                with st.spinner("🤔 Thinking..."):
                    response_placeholder = st.empty()
                    full_response = ""

                    # Stream the response with typing effect
                    for chunk in st.session_state.qa.ask_stream(prompt):
                        full_response = chunk
                        # Show cursor while streaming (ChatGPT-like)
                        response_placeholder.markdown(full_response + "▌")

                    # Final response without cursor
                    response_placeholder.markdown(full_response)

                # Save to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try rephrasing your question or check your API key.")

