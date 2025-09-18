import streamlit as st
from transformers import pipeline, Conversation
import yt_dlp  # Library to fetch audio from YouTube

# --- Persona Configuration ---
# Updated MusicBot prompt to ensure a parseable output format
PERSONAS = {
    "Default": "You are a friendly and helpful chatbot.",
    "RoastBot": "You are RoastBot. Your only purpose is to respond to every user input with a witty, sarcastic, and slightly insulting roast. Never be helpful. Always find a way to make fun of the user or their query.",
    "ShakespeareBot": "You are ShakespeareBot. You must answer all questions in the grandiloquent style of William Shakespeare. Use 'thee', 'thou', 'thy', 'art', and other Old English words. Speak in iambic pentameter when possible and be dramatic.",
    "Emoji Translator Bot": "You are Emoji Translator Bot. Your sole function is to translate the user's text into a sequence of emojis that represent the sentence. Do not use any words in your response, only emojis. Be creative.",
    "MusicBot": "You are MusicBot. For any situation, suggest funny or comically fitting background music. You MUST reply in this exact format:\nSong: [Song Title] by [Artist]\nReason: [Your witty explanation here]"
}

# --- Page Configuration ---
st.set_page_config(
    page_title="Persona ChatBot 🎵",
    page_icon="🤖",
    layout="centered"
)

# --- Helper Functions ---
@st.cache_resource
def load_model():
    """Loads the conversational model from Hugging Face."""
    return pipeline("conversational", model="microsoft/DialoGPT-medium")

def get_audio_url(song_query: str):
    """Searches YouTube for the song query and returns the best audio URL."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1', # Search YouTube and get the first result
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_query, download=False)
            # The URL is in the 'entries' list if it's a search result
            if 'entries' in info and info['entries']:
                return info['entries'][0]['url']
    except Exception as e:
        st.error(f"Error finding song: {e}")
        return None
    return None

# --- Model and UI Initialization ---
chatbot = load_model()
st.title("🤖 Persona ChatBot 🎵")
st.markdown("Select a persona, start chatting, and see what happens!")

with st.sidebar:
    st.header("Settings")
    selected_persona = st.selectbox("Choose a Persona:", options=list(PERSONAS.keys()))
    if st.button("Clear Conversation"):
        st.session_state.clear()
        st.rerun()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation' not in st.session_state:
    st.session_state.conversation = None

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Chat Logic ---
if prompt := st.chat_input("What's on your mind?"):
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare conversation for the model
    if st.session_state.conversation is None:
        system_prompt = PERSONAS[selected_persona]
        st.session_state.conversation = Conversation(f"{system_prompt}\nUser: {prompt}")
    else:
        st.session_state.conversation.add_user_input(prompt)

    # Generate bot response
    with st.spinner("Thinking..."):
        response = chatbot(st.session_state.conversation)
        bot_response = response.generated_responses[-1]

    # Add and display bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

        # --- MusicBot audio playback logic ---
        if selected_persona == "MusicBot" and "song:" in bot_response.lower():
            try:
                # Extract the song title and artist from the specific format
                song_line = [line for line in bot_response.split('\n') if line.lower().startswith('song:')][0]
                song_query = song_line.split(':', 1)[1].strip()

                with st.spinner(f"Finding '{song_query}'... 🎶"):
                    audio_url = get_audio_url(song_query)
                
                if audio_url:
                    st.audio(audio_url, format='audio/webm')
                    st.caption("Here's a sample of the track! (Full track may play)")
                else:
                    st.warning("Sorry, I couldn't find a playable version of that song.")
            except IndexError:
                # This handles cases where the model didn't follow the format perfectly
                st.info("The bot suggested a song, but I couldn't parse the title.")
