#modified from https://lablab.ai/t/vectara-chat-essentials-harness-ai-for-next-gen-hackathon-chatbot 

import os
import json
import logging
import requests
import streamlit as st
from streamlit_chat import message

from dotenv import load_dotenv

load_dotenv()

def get_latest_conversation_id(api_key, customer_id):
    """Retrieves the latest conversation ID from Vectara."""
    response = requests.post(
        "https://api.vectara.io/v1/list-conversations",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "customer-id": customer_id,
            "x-api-key": api_key,
        },
        data=json.dumps({"numResults": 0, "pageKey": ""}),
    )
    response_data = response.json()
    return (
        response_data["conversation"][-1]["conversationId"]
        if response_data and "conversation" in response_data
        else None
    )

st.session_state["corpus_number"] = os.getenv('VECTARA_CORPUS_ID')
st.session_state["vectara_api_key"] = os.getenv('VECTARA_API_KEY ')

# Configure logging for better tracking
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Streamlit page configuration
st.set_page_config(page_title="Duke AI Chatbot", page_icon="💬")

# Chat message handling
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.form("chat_input", clear_on_submit=True):
    user_prompt = st.text_input("Your message:", label_visibility="collapsed")

    if st.form_submit_button("Send"):
        st.session_state.messages.append({"role": "user", "content": user_prompt})

# Display chat messages
for idx, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=f"chat_message_{idx}")
