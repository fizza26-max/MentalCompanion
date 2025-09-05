import streamlit as st
from transformers import pipeline
from transformers.conversation import Conversation
from datetime import datetime

# --- Load model with caching ---
@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline("conversational", model="microsoft/DialoGPT-small")

try:
    conversational_pipeline = load_model()
except KeyError:
    st.error(
        "Your transformers version does not support the 'conversational' pipeline. "
        "Please upgrade transformers to version 4.5.0 or higher."
    )
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- Helper functions ---

def generate_response(user_input):
    conv = Conversation(user_input)
    result = conversational_pipeline(conv)
    return result.generated_responses[-1]

def mood_emoji(mood):
    emojis = {
        "Happy": "😊",
        "Sad": "😢",
        "Anxious": "😰",
        "Angry": "😠",
        "Neutral": "😐"
    }
    return emojis.get(mood, "🙂")

# --- Streamlit App ---

st.set_page_config(page_title="Mental Wellness Companion", page_icon="🧠")

st.title("🧠 Mental Wellness Companion")
st.markdown("""
Welcome! This companion is here to listen, offer coping strategies, track your mood, and provide helpful resources.  
*Note: This tool is not a substitute for professional mental health care.*
""")

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

# Mood tracking input
with st.expander("🌡️ Track Your Mood"):
    mood = st.selectbox("How are you feeling right now?", ["Happy", "Sad", "Anxious", "Angry", "Neutral"])
    if st.button("Log Mood"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.mood_log.append({"mood": mood, "time": timestamp})
        st.success(f"Mood '{mood}' logged at {timestamp} {mood_emoji(mood)}")

# Display mood history
if st.session_state.mood_log:
    st.subheader("📊 Mood History")
    for entry in reversed(st.session_state.mood_log[-5:]):  # show last 5 entries
        st.write(f"{entry['time']}: {entry['mood']} {mood_emoji(entry['mood'])}")

st.markdown("---")

# Chat interface
st.subheader("💬 Chat with your companion")

user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input.strip():
    # Append user message
    st.session_state.conversation.append({"role": "user", "text": user_input})

    # Generate AI response
    try:
        response = generate_response(user_input)
    except Exception:
        response = "Sorry, I'm having trouble responding right now."

    # Append bot response
    st.session_state.conversation.append({"role": "bot", "text": response})

# Display conversation
for chat in st.session_state.conversation:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['text']}")
    else:
        st.markdown(f"**Companion:** {chat['text']}")

st.markdown("---")
st.markdown("""
### Privacy & Ethics
- Your data is stored only during this session and not shared or saved externally.
- This companion is not a replacement for professional help.
- If you are in crisis, please contact emergency services or a trusted professional immediately.
""")
