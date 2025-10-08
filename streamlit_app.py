import streamlit as st
from src.app import YouTubeQA

st.set_page_config(page_title="YouTube Q&A", page_icon="🎥", layout="wide")

# Initialize session state
if 'qa' not in st.session_state:
    st.session_state.qa = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'ready' not in st.session_state:
    st.session_state.ready = False
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7  # Default temperature

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # API Key Section
    api_key = st.text_input("Groq API Key:", type="password")
    if st.button("Set API Key"):
        if api_key:
            st.session_state.qa = YouTubeQA(api_key, st.session_state.temperature)
            st.success("✅ API key set!")

    st.divider()

    # Temperature Control
    st.subheader("🌡️ Temperature")

    # Temperature slider with explanation
    temperature = st.slider(
        "Response Randomness",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
        help="Controls creativity vs consistency:\n"
             "• 0.0 = Deterministic, focused\n"
             "• 0.7 = Balanced (recommended)\n"
             "• 1.0 = Creative, diverse"
    )

    # Update temperature if changed
    if temperature != st.session_state.temperature:
        st.session_state.temperature = temperature
        if st.session_state.qa:
            try:
                st.session_state.qa.set_temperature(temperature)
                st.success(f"✅ Temperature updated to {temperature}")
            except Exception as e:
                st.error(f"Error updating temperature: {e}")

    # Show current temperature
    st.caption(f"Current: {st.session_state.temperature}")

    st.divider()

    video_url = st.text_input("YouTube URL:")
    if st.button("Load Video"):
        if not st.session_state.qa:
            st.warning("⚠️ Set API key first!")
        elif video_url:
            with st.spinner("Loading video..."):
                if st.session_state.qa.load_video(video_url):
                    st.session_state.ready = True
                    st.success("✅ Video loaded!")
                else:
                    st.error("❌ Failed to load video")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

# Main chat interface
st.title("🎥 YouTube Video Q&A")

if not st.session_state.ready:
    st.info("👈 Configure the system in the sidebar to get started!")
else:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about the video..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Stream the response
                response_placeholder = st.empty()
                full_response = ""

                for chunk in st.session_state.qa.ask_stream(prompt):
                    full_response = chunk  # Each chunk is the full response so far
                    response_placeholder.markdown(full_response + "▌")

                # Final response without cursor
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {e}")

