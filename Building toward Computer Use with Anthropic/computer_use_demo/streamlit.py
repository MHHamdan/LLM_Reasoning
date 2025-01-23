import asyncio
import os
import traceback
from datetime import datetime, timedelta
from contextlib import contextmanager
from typing import cast

import openai
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit_chat import st_chat_message  # Custom chat message renderer if applicable

from openai_sampling_loop import sampling_loop

CONFIG_DIR = os.path.expanduser("~/.openai")
API_KEY_FILE = os.path.join(CONFIG_DIR, "api_key")

STREAMLIT_STYLE = """
<style>
    /* Highlight the stop button in red */
    button[kind=header] {
        background-color: rgb(255, 75, 75);
        border: 1px solid rgb(255, 75, 75);
        color: rgb(255, 255, 255);
    }
    button[kind=header]:hover {
        background-color: rgb(255, 51, 51);
    }
     /* Hide the streamlit deploy button */
    .stAppDeployButton {
        visibility: hidden;
    }
</style>
"""

class Sender:
    USER = "user"
    BOT = "assistant"

def setup_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = load_from_storage("api_key") or os.getenv("OPENAI_API_KEY", "")
    if "model" not in st.session_state:
        st.session_state.model = "gpt-4"
    if "auth_validated" not in st.session_state:
        st.session_state.auth_validated = False
    if "in_sampling_loop" not in st.session_state:
        st.session_state.in_sampling_loop = False

def load_from_storage(filename: str) -> str | None:
    try:
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return file.read().strip()
    except Exception as e:
        st.write(f"Error loading {filename}: {e}")
    return None

def save_to_storage(filename: str, data: str):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            file.write(data)
    except Exception as e:
        st.write(f"Error saving {filename}: {e}")

def validate_auth(api_key: str | None):
    if not api_key:
        return "Enter your OpenAI API key in the sidebar to continue."
    try:
        openai.api_key = api_key
        openai.Model.list()
    except openai.error.AuthenticationError:
        return "Invalid OpenAI API key. Please check your credentials."
    except Exception as e:
        return f"Unexpected error: {e}"
    return None

@contextmanager
def track_sampling_loop():
    st.session_state.in_sampling_loop = True
    yield
    st.session_state.in_sampling_loop = False

async def main():
    setup_state()

    st.markdown(STREAMLIT_STYLE, unsafe_allow_html=True)
    st.title("OpenAI GPT Chat Demo")

    with st.sidebar:
        st.text_input(
            "OpenAI API Key",
            type="password",
            key="api_key",
            on_change=lambda: save_to_storage(API_KEY_FILE, st.session_state.api_key),
        )
        st.text_input("Model", key="model")

        if st.button("Reset", type="primary"):
            st.session_state.clear()
            setup_state()

    if not st.session_state.auth_validated:
        if auth_error := validate_auth(st.session_state.api_key):
            st.warning(f"Please resolve the following auth issue:\n\n{auth_error}")
            return
        else:
            st.session_state.auth_validated = True

    chat_tab, logs_tab = st.tabs(["Chat", "Logs"])

    with chat_tab:
        new_message = st.chat_input("Type a message...")

        for message in st.session_state.messages:
            _render_message(message["role"], message["content"])

        if new_message:
            st.session_state.messages.append({"role": Sender.USER, "content": new_message})
            _render_message(Sender.USER, new_message)

            with track_sampling_loop():
                try:
                    st.session_state.messages = await sampling_loop(
                        api_key=st.session_state.api_key,
                        model=st.session_state.model,
                        messages=st.session_state.messages,
                        output_callback=lambda content: _render_message(Sender.BOT, content),
                    )
                except Exception as e:
                    st.error(f"Error during sampling loop: {e}")


def _render_message(sender: str, content: str):
    if sender == Sender.USER:
        st.chat_message("user", content)
    else:
        st.chat_message("assistant", content)

if __name__ == "__main__":
    asyncio.run(main())
