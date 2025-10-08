import streamlit as st
from src.app import YouTubeQA
import time

# ChatGPT-like page configuration
st.set_page_config(
    page_title="YouTube Q&A Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar visible by default
)

# Initialize theme state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Default to dark theme like ChatGPT

# Theme colors
THEMES = {
    'dark': {
        'bg': '#343541',
        'secondary_bg': '#40414f',
        'sidebar_bg': '#202123',
        'text': '#ececec',
        'text_secondary': '#c5c5d2',
        'border': '#565869',
        'input_bg': '#40414f',
        'accent': '#19c37d',
        'user_msg': '#343541',
        'assistant_msg': '#444654',
    },
    'light': {
        'bg': '#ffffff',
        'secondary_bg': '#f7f7f8',
        'sidebar_bg': '#f9f9f9',
        'text': '#2d2d2d',
        'text_secondary': '#6e6e80',
        'border': '#d1d5db',
        'input_bg': '#ffffff',
        'accent': '#10a37f',
        'user_msg': '#f7f7f8',
        'assistant_msg': '#ffffff',
    }
}

theme = THEMES[st.session_state.theme]

# Custom CSS for ChatGPT-like styling with theme support
st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global styles */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Main app background */
    .stApp {{
        background-color: {theme['bg']};
    }}

    /* Main chat container */
    .main .block-container {{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 48rem !important;
        margin: 0 auto !important;
    }}

    /* Remove default padding */
    .main {{
        padding: 0 !important;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {theme['sidebar_bg']} !important;
        border-right: 1px solid {theme['border']};
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background-color: {theme['sidebar_bg']} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: {theme['text']} !important;
    }}

    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p {{
        color: {theme['text']} !important;
    }}

    /* Sidebar text inputs */
    [data-testid="stSidebar"] input[type="text"],
    [data-testid="stSidebar"] input[type="password"] {{
        background-color: {theme['input_bg']} !important;
        color: {theme['text']} !important;
        border: 2px solid {theme['border']} !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
    }}

    [data-testid="stSidebar"] input[type="text"]:focus,
    [data-testid="stSidebar"] input[type="password"]:focus {{
        border-color: {theme['accent']} !important;
        box-shadow: 0 0 0 2px rgba(25, 195, 125, 0.2) !important;
        outline: none !important;
    }}

    [data-testid="stSidebar"] input::placeholder {{
        color: {theme['text_secondary']} !important;
        opacity: 0.8 !important;
    }}

    /* Sidebar buttons */
    [data-testid="stSidebar"] button[kind="primary"],
    [data-testid="stSidebar"] button[kind="secondary"] {{
        background-color: {theme['accent']} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s !important;
    }}

    [data-testid="stSidebar"] button:hover {{
        opacity: 0.85 !important;
        transform: translateY(-1px) !important;
    }}

    /* Theme toggle button - special styling */
    [data-testid="stSidebar"] button[key="theme_toggle"] {{
        background-color: {theme['secondary_bg']} !important;
        color: {theme['text']} !important;
        border: 1px solid {theme['border']} !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 1.2rem !important;
    }}

    /* Sidebar slider */
    [data-testid="stSidebar"] .stSlider {{
        padding: 1rem 0 !important;
    }}

    [data-testid="stSidebar"] .stSlider > div > div > div {{
        background-color: {theme['border']} !important;
    }}

    [data-testid="stSidebar"] .stSlider > div > div > div > div {{
        background-color: {theme['accent']} !important;
    }}

    /* Sidebar captions */
    [data-testid="stSidebar"] .stCaption {{
        color: {theme['text_secondary']} !important;
        font-size: 0.85rem !important;
    }}

    /* Sidebar expander */
    [data-testid="stSidebar"] [data-testid="stExpander"] {{
        background-color: {theme['secondary_bg']} !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 8px !important;
    }}

    [data-testid="stSidebar"] [data-testid="stExpander"] summary {{
        color: {theme['text']} !important;
        font-size: 0.9rem !important;
    }}

    /* Sidebar divider */
    [data-testid="stSidebar"] hr {{
        border-color: {theme['border']} !important;
        opacity: 0.3 !important;
        margin: 1.5rem 0 !important;
    }}

    /* Sidebar success/error/info messages */
    [data-testid="stSidebar"] .stAlert {{
        background-color: {theme['secondary_bg']} !important;
        border: 1px solid {theme['border']} !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 0.85rem !important;
    }}

    /* Sidebar labels */
    [data-testid="stSidebar"] label {{
        color: {theme['text']} !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }}

    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Title styling */
    h1 {{
        color: {theme['text']} !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin: 0 !important;
        padding: 1.25rem 1.5rem !important;
        text-align: center !important;
        border-bottom: 1px solid {theme['border']} !important;
        background-color: {theme['bg']} !important;
    }}

    /* Chat messages */
    .stChatMessage {{
        background-color: transparent !important;
        padding: 2rem 1.5rem !important;
        border-radius: 0 !important;
        margin-bottom: 0 !important;
    }}

    /* User message background */
    .stChatMessage[data-testid*="user"] {{
        background-color: {theme['user_msg']} !important;
        border-bottom: 1px solid {theme['border']} !important;
    }}

    /* Assistant message background */
    .stChatMessage[data-testid*="assistant"] {{
        background-color: {theme['assistant_msg']} !important;
        border-bottom: 1px solid {theme['border']} !important;
    }}

    /* Message text color */
    .stChatMessage p {{
        color: {theme['text']} !important;
        line-height: 1.75 !important;
        font-size: 1rem !important;
        margin: 0 !important;
        font-weight: 400 !important;
    }}

    /* Message avatar */
    .stChatMessage [data-testid="chatAvatarIcon"] {{
        width: 36px !important;
        height: 36px !important;
        font-size: 1.5rem !important;
    }}

    /* Chat input styling */
    .stChatFloatingInputContainer {{
        background-color: {theme['bg']} !important;
        border-top: 1px solid {theme['border']};
        padding: 1.5rem 1rem 1.5rem 1rem !important;
    }}

    /* Chat input container */
    .stChatInputContainer {{
        background-color: transparent !important;
        max-width: 48rem !important;
        margin: 0 auto !important;
    }}

    /* Chat input wrapper */
    .stChatInput {{
        background-color: {theme['input_bg']} !important;
        border: 2px solid {theme['border']} !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        transition: all 0.2s ease !important;
    }}

    .stChatInput:focus-within {{
        border-color: {theme['accent']} !important;
        box-shadow: 0 4px 16px rgba(25, 195, 125, 0.3) !important;
    }}

    /* Chat input textarea */
    .stChatInput textarea {{
        background-color: {theme['input_bg']} !important;
        color: {theme['text']} !important;
        font-size: 1rem !important;
        padding: 1rem 1.25rem !important;
        line-height: 1.5 !important;
        min-height: 24px !important;
        max-height: 200px !important;
        font-weight: 400 !important;
    }}

    .stChatInput textarea::placeholder {{
        color: {theme['text_secondary']} !important;
        opacity: 0.8 !important;
        font-size: 1rem !important;
    }}

    /* Chat input send button */
    .stChatInput button {{
        background-color: transparent !important;
        color: {theme['text_secondary']} !important;
        border: none !important;
        padding: 0.5rem !important;
        transition: all 0.2s ease !important;
    }}

    .stChatInput button:hover {{
        color: {theme['accent']} !important;
        transform: scale(1.1) !important;
    }}

    .stChatInput button:disabled {{
        opacity: 0.3 !important;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: {theme['accent']} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }}

    .stButton > button:hover {{
        opacity: 0.85 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
    }}

    .stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* Text inputs */
    .stTextInput input {{
        background-color: {theme['input_bg']} !important;
        color: {theme['text']} !important;
        border: 1.5px solid {theme['border']} !important;
        border-radius: 8px !important;
        padding: 0.6rem !important;
        font-size: 0.95rem !important;
    }}

    .stTextInput input:focus {{
        border-color: {theme['accent']} !important;
        box-shadow: 0 0 0 1px {theme['accent']} !important;
    }}

    .stTextInput input::placeholder {{
        color: {theme['text_secondary']} !important;
        opacity: 0.6 !important;
    }}

    /* Sliders */
    .stSlider {{
        padding: 1rem 0 !important;
    }}

    .stSlider > div > div > div {{
        background-color: {theme['border']} !important;
        height: 4px !important;
    }}

    .stSlider > div > div > div > div {{
        background-color: {theme['accent']} !important;
    }}

    .stSlider > div > div > div > div > div {{
        background-color: {theme['accent']} !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
    }}

    /* Info boxes */
    .stAlert {{
        background-color: {theme['secondary_bg']};
        color: {theme['text']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
    }}

    /* Spinner */
    .stSpinner > div {{
        border-color: {theme['accent']} !important;
    }}

    /* Divider */
    hr {{
        border-color: {theme['border']};
        margin: 1rem 0;
    }}

    /* Welcome screen */
    .welcome-container {{
        text-align: center;
        padding: 3rem 1rem;
        color: {theme['text']};
    }}

    .welcome-title {{
        font-size: 2rem;
        font-weight: 700;
        color: {theme['accent']};
        margin-bottom: 1rem;
    }}

    .welcome-subtitle {{
        font-size: 1.1rem;
        color: {theme['text_secondary']};
        margin-bottom: 3rem;
    }}

    .step-card {{
        text-align: center;
        padding: 1.5rem;
        background-color: {theme['secondary_bg']};
        border-radius: 12px;
        border: 1px solid {theme['border']};
        transition: all 0.2s;
    }}

    .step-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}

    .step-icon {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }}

    .step-title {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {theme['text']};
        margin-bottom: 0.5rem;
    }}

    .step-desc {{
        color: {theme['text_secondary']};
        font-size: 0.9rem;
    }}

    /* Theme toggle button */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background-color: {theme['secondary_bg']};
        border: 1px solid {theme['border']};
        border-radius: 20px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }}

    .theme-toggle:hover {{
        transform: scale(1.05);
    }}
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

# Sidebar (ChatGPT-style)
with st.sidebar:
    # Header with theme toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<h3 style='margin-top: 0; color: {theme['text']};'>⚙️ Settings</h3>", unsafe_allow_html=True)
    with col2:
        theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
        if st.button(theme_icon, key="theme_toggle", help="Toggle dark/light theme"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()

    st.divider()

    # API Key Section
    st.markdown(f"""
    <div style='margin-bottom: 0.75rem;'>
        <p style='font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; color: {theme['text']};'>
            🔑 API Configuration
        </p>
    </div>
    """, unsafe_allow_html=True)

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API key...",
        help="Get your API key from https://console.groq.com",
        label_visibility="collapsed"
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
    st.markdown(f"""
    <div style='margin-bottom: 0.75rem;'>
        <p style='font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; color: {theme['text']};'>
            🎥 Video Source
        </p>
    </div>
    """, unsafe_allow_html=True)

    video_url = st.text_input(
        "YouTube URL",
        value=st.session_state.video_url,
        placeholder="https://youtube.com/watch?v=...",
        help="Paste a YouTube video URL to analyze",
        label_visibility="collapsed"
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
                    success = st.session_state.qa.load_video(video_url)
                    if success:
                        # Sync ready state from qa object
                        st.session_state.ready = st.session_state.qa.ready
                        st.session_state.video_url = video_url
                        st.success("✅ Video loaded successfully!")
                        time.sleep(0.5)
                        st.rerun()  # Rerun to update UI
                    else:
                        st.session_state.ready = False
                        st.error("❌ Failed to load video. Please check the URL.")
                except Exception as e:
                    st.session_state.ready = False
                    st.error(f"❌ Error: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())
                finally:
                    st.session_state.processing = False

    # Show loaded video info
    if st.session_state.ready and st.session_state.video_url:
        st.success("📺 Video loaded and ready!")

    # Sync ready state with qa object if it exists
    if st.session_state.qa and hasattr(st.session_state.qa, 'ready'):
        st.session_state.ready = st.session_state.qa.ready

    st.divider()

    # Temperature Control
    st.markdown(f"""
    <div style='margin-bottom: 0.75rem;'>
        <p style='font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; color: {theme['text']};'>
            🌡️ Model Settings
        </p>
    </div>
    """, unsafe_allow_html=True)

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
        help="Lower = more focused, Higher = more creative",
        label_visibility="collapsed"
    )

    st.markdown(f"<p style='font-size: 0.85rem; color: {theme['text_secondary']}; margin-top: 0.5rem;'>Current: {temperature}</p>", unsafe_allow_html=True)

    # Update temperature if changed
    if temperature != st.session_state.temperature:
        st.session_state.temperature = temperature
        if st.session_state.qa:
            try:
                st.session_state.qa.set_temperature(temperature)
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
    st.markdown(f"""
    <div style='margin-bottom: 0.75rem;'>
        <p style='font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; color: {theme['text']};'>
            💬 Chat Controls
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat cleared!")
        time.sleep(0.3)
        st.rerun()

    # Stats
    if st.session_state.messages:
        msg_count = len(st.session_state.messages)
        st.markdown(f"<p style='font-size: 0.85rem; color: {theme['text_secondary']}; margin-top: 0.75rem;'>💬 {msg_count} message{'s' if msg_count != 1 else ''} in chat</p>", unsafe_allow_html=True)

# Main chat interface - ChatGPT style
st.markdown(f"<h1 style='color: {theme['text']}; text-align: center; padding: 1rem 0; margin: 0;'>💬 YouTube Video Q&A</h1>", unsafe_allow_html=True)

# Welcome message or chat interface
if not st.session_state.ready:
    # Welcome screen (ChatGPT-like)
    st.markdown(f"""
    <div class='welcome-container'>
        <div class='welcome-title'>Welcome to YouTube Video Q&A</div>
        <div class='welcome-subtitle'>Ask questions about any YouTube video using AI</div>
    </div>
    """, unsafe_allow_html=True)

    # Getting started steps
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class='step-card'>
            <div class='step-icon'>🔑</div>
            <div class='step-title'>1. Set API Key</div>
            <div class='step-desc'>Enter your Groq API key in the sidebar</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='step-card'>
            <div class='step-icon'>🎥</div>
            <div class='step-title'>2. Load Video</div>
            <div class='step-desc'>Paste a YouTube URL and click Load</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='step-card'>
            <div class='step-icon'>💬</div>
            <div class='step-title'>3. Start Chatting</div>
            <div class='step-desc'>Ask questions about the video content</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Open the sidebar to get started!", icon="ℹ️")

# Always show chat history below (even before ready)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Chat input at bottom (always visible)
if prompt := st.chat_input("Message YouTube Q&A...", key="chat_input"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Check if system is ready
    if not st.session_state.qa:
        with st.chat_message("assistant", avatar="🤖"):
            msg = "⚠️ Please set your Groq API key in the sidebar first."
            st.markdown(msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": msg
            })
    elif not st.session_state.ready or not st.session_state.qa.ready:
        with st.chat_message("assistant", avatar="🤖"):
            msg = "⚠️ Please load a YouTube video URL in the sidebar first. Once loaded, I'll be able to answer your questions about the video!"
            st.markdown(msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": msg
            })
    else:
        # Generate assistant response with loading animation
        with st.chat_message("assistant", avatar="🤖"):
            try:
                # Show loading indicator
                with st.spinner(""):
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

