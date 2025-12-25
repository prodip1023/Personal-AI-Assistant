import streamlit as st
import time,os,io
import base64
from datetime import datetime
from auth.auth_manager import AuthManager
from jarvis.memory import Memory
from jarvis.prompt_controller import PromptController
from jarvis.gemini_engine import GeminiEngine
from jarvis.assistant import JarvisAssistant
from config.settings import APIKey
from loggin.logger import setup_logger
from utils.export_chat_pdf import export_pdf,export_text
from utils.voice_input import listen
from PIL import Image





def init_session_state():
    defaults = {
        "login": False,
        "current_user": "",
        "chat_history": [],
        "is_processing": False,
        "current_chat_id": f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "all_chats": {},
        "uploaded_files": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# Create chat if not exists
chat_id = st.session_state.current_chat_id

if chat_id not in st.session_state.all_chats:
    st.session_state.all_chats[chat_id] = {
        "name": "New Chat",
        "messages": [],
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M')
    }


st.set_page_config("PERSONAL AI ASSISTANT",page_icon="🤖",layout='centered')

