import streamlit as st
import requests

st.title("Gitops Consolidator Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat UI loop
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    # Send to Google ADK backend (replace URL and payload with your ADK endpoint details)
    response = requests.post(
        "http://your-adk-backend-url/agent/chat",
        json={"message": user_input}
    )
    # Parse ADK's response
    adk_reply = response.json().get("reply", "Sorry, I couldn't process that.")
    st.session_state.chat_history.append({"role": "assistant", "content": adk_reply})
    st.experimental_rerun()
