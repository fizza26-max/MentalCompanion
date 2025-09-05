import streamlit as st
from datetime import datetime

# --- Helper functions ---

def generate_response(user_input, mood):
    """
    Simulated empathetic response generator.
    Replace this with your fine-tuned open-source model inference.
    """
    user_input = user_input.lower()
    if any(word in user_input for word in ["sad", "down", "unhappy", "depressed"]):
        return ("I'm sorry to hear you're feeling this way. "
                "Remember, it's okay to have tough days. "
                "Would you like some coping strategies or resources?")
    elif any(word in user_input for word in ["anxious", "nervous", "worried"]):
        return ("Anxiety can be overwhelming. "
                "Deep breathing and grounding exercises might help. "
                "Would you like me to guide you through one?")
    elif "coping" in user_input:
        return ("Here are some coping strategies:\n"
                "- Practice deep breathing\n"
                "- Take a short walk\n"
                "- Write down your thoughts\n"
                "- Reach out to a trusted friend\n"
                "Would you like resources for professional help?")
    elif "resource" in user_input or "help" in user_input:
        return ("Here are some resources you might find helpful:\n"
                "- National Suicide Prevention Lifeline: 1-800-273-8255\n"
                "- Crisis Text Line: Text HOME to 741741\n"
                "- MentalHealth.gov: https://www.mentalhealth.gov\n"
                "Remember, seeking help is a sign of strength.")
    else:
        return ("Thank you for sharing. How are you feeling today? "
                "You can tell me about your mood or ask for coping strategies.")

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

# Session state for conversation and mood tracking
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

    # Generate response based on last mood logged or neutral if none
    last_mood = st.session_state.mood_log[-1]["mood"] if st.session_state.mood_log else "Neutral"
    response = generate_response(user_input, last_mood)

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
