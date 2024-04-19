import os
import json
import logging
import requests
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from getpass import getpass
from huggingface_hub import HfApi

load_dotenv()

st.session_state["corpus_number"] = st.secrets["VECTARA_CORPUS_ID"]
st.session_state["vectara_api_key"] = st.secrets["VECTARA_API_KEY"]
st.session_state["vectara_customer_id"] = st.secrets["VECTARA_CUSTOMER_ID"]
st.session_state["hf_model_id"] = st.secrets["HF_MODEL_ID"]
st.session_state["hf_token"] = st.secrets["HF_TOKEN"]

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

def get_vectara_results(query):
    """Queries the Vectara API and retrieves semantic search results."""
    response = requests.post(
        "https://api.vectara.io:443/v1/stream-query",
        headers={
            "Content-Type": "application/json",
            "authorization": "Bearer " + st.session_state["vectara_api_key"],
            "customer-id": st.session_state["vectara_customer_id"],
        },
        json={
            "query": [
                {
                    "query": query,
                    "queryContext": "",
                    "start": 0,
                    "numResults": 10,
                    "contextConfig": {
                        "charsBefore": 0,
                        "charsAfter": 0,
                        "sentencesBefore": 2,
                        "sentencesAfter": 2,
                        "startTag": "%START_SNIPPET%",
                        "endTag": "%END_SNIPPET%",
                    },
                    "corpusKey": [
                        {
                            "customerId": st.session_state["vectara_customer_id"],
                            "corpusId": st.session_state["corpus_number"],
                            "semantics": 0,
                            "metadataFilter": "",
                            "lexicalInterpolationConfig": {"lambda": 0.025},
                            "dim": [],
                        }
                    ],
                    "summary": [],
                }
            ]
        },
    )
    return response.json()

def chat_with_model(prompt, context):
    api = HfApi()
    model_id = st.session_state["hf_model_id"]
    token = st.session_state["hf_token"]
    model = api.model_info(repo_id=model_id, token=token)
    pipeline = model.pipeline_type
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"inputs": prompt, "options": {"use_cache": False}, "parameters": {"context": context}},
    )
    return response.json()[0]["generated_text"]

# Streamlit page configuration
st.set_page_config(page_title="Duke AI Chatbot", page_icon="💬")

# Add logo and title
st.image("assets/logo.png", use_column_width=True)
st.title("Duke AI Chatbot")
st.markdown("Welcome to the Duke AI chatbot. I can answer any of your questions about the Duke M.Eng. AI program!")
st.markdown("By Aryan Poonacha for AIPI 590 - Spring '24")
url = 'https://duke.qualtrics.com/jfe/form/SV_9ZAdIFH74vz6O46'
st.markdown("Provide Feedback Here!" % url)

# Chat message handling
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.form("chat_input", clear_on_submit=True):
    user_prompt = st.text_input("Your message:", label_visibility="collapsed")
    if st.form_submit_button("Send"):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        vectara_results = get_vectara_results(user_prompt)
        model_response = chat_with_model(user_prompt, vectara_results)
        st.session_state.messages.append({"role": "assistant", "content": model_response})

# Display chat messages
for idx, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=f"chat_message_{idx}")
