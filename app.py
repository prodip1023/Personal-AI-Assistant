import streamlit as st
import time
from datetime import datetime

from auth.auth_manager import AuthManager
from jarvis.memory import Memory
from jarvis.prompt_controller import PromptController
from jarvis.gemini_engine import GeminiEngine
from config.settings import APIKey
from utils.voice_input import listen
from utils.export_chat_pdf import export_pdf,export_text
from jarvis.assistant import JarvisAssistant


# ==========================
# PAGE CONFIG (MUST BE FIRST)
# ==========================
st.set_page_config(
    page_title="JARVIS AI",
    page_icon="🤖",
    layout="wide"
)


# ==========================
# SESSION STATE
# ==========================
def init_state():
    defaults = {
        "login": False,
        "current_user": "",
        "chat_history": [],
        "current_chat_id": f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "all_chats": {},
        "is_processing": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

if st.session_state.current_chat_id not in st.session_state.all_chats:
    st.session_state.all_chats[st.session_state.current_chat_id] = {
        "name": "New Chat",
        "messages": [],
        "created_at": datetime.now().strftime("%d %b %Y %H:%M")
    }


# ==========================
# CLEAN MODERN UI STYLE
# ==========================
st.markdown("""
<style>

/* -------- GLOBAL -------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* -------- APP BACKGROUND -------- */
.stApp {
    background: linear-gradient(135deg, #EEF2FF, #E0F2FE);
    color: #334155;
}

/* -------- SIDEBAR -------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #312E81, #3730A3);
    border-right: 1px solid #4338CA;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #E0E7FF !important;
}

/* Sidebar card */
.sidebar-card {
    background: linear-gradient(135deg, #4338CA, #6366F1);
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 14px;
    box-shadow: 0 10px 25px rgba(67,56,202,0.35);
}

/* -------- TITLE -------- */
.title {
    font-size: 1.9rem;
    font-weight: 600;
    color: #3730A3;
    margin-bottom: 6px;
}

/* -------- CHAT USER -------- */
.chat-user {
    background: linear-gradient(135deg, #06B6D4, #0EA5E9);
    color: #ECFEFF;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 10px 0;
    max-width: 72%;
    margin-left: auto;
    box-shadow: 0 10px 22px rgba(14,165,233,0.35);
    font-size: 0.95rem;
}

/* -------- CHAT AI -------- */
.chat-ai {
    background: linear-gradient(135deg, #DDD6FE, #EDE9FE);
    color: #4C1D95;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 10px 0;
    max-width: 72%;
    margin-right: auto;
    box-shadow: 0 10px 22px rgba(139,92,246,0.25);
    font-size: 0.95rem;
}

/* -------- BUTTONS -------- */
.stButton > button {
    background: linear-gradient(135deg, #8B5CF6, #6366F1);
    color: #EEF2FF;
    border-radius: 12px;
    border: none;
    padding: 10px 16px;
    font-weight: 500;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 20px rgba(99,102,241,0.4);
}

/* -------- INPUT BOX -------- */
textarea {
    background: linear-gradient(135deg, #E0E7FF, #DBEAFE) !important;
    color: #3730A3 !important;
    border-radius: 14px !important;
    border: 1px solid #A5B4FC !important;
}

/* -------- FILE UPLOADER -------- */
section[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #EDE9FE, #DDD6FE);
    padding: 12px;
    border-radius: 12px;
    border: 1px dashed #A78BFA;
}

/* -------- TABS -------- */
.stTabs [role="tab"] {
    background: transparent;
    color: #6D28D9;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    color: #4338CA;
    border-bottom: 2px solid #6366F1;
}

</style>
""", unsafe_allow_html=True)




auth = AuthManager()


# ==========================
# LOGIN / REGISTER
# ==========================
if not st.session_state.login:

    st.markdown("<div class='title'>🤖 JARVIS AI</div>", unsafe_allow_html=True)
    st.caption("Secure Personal AI Assistant")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        username = st.text_input("email",key="login_user",placeholder="Enter your email")
        password = st.text_input("Password", type="password",key="login_pass",placeholder="Enter your password")
        if st.button("Login", use_container_width=True):
            if auth.login(username, password):
                st.session_state.login = True
                st.session_state.current_user = username
                st.success("Login successful")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New email",key="reg_user",placeholder="Select new email")
        new_pass = st.text_input("Password", type="password",key="reg_pass",placeholder="Enter password")
        confirm_pass = st.text_input("Confirm Password", type="password",key="confirm_pass",placeholder="Enter confirm password")
        if st.button("Register", use_container_width=True):
            if new_pass != confirm_pass:
                st.error("Passwords do not match")
            elif auth.register(new_user, new_pass):
                st.success("Account created")
            else:
                st.error("User already exists")

    st.stop()


# ==========================
# SIDEBAR
# ==========================
with st.sidebar:

    st.markdown(f"""
    <div class="sidebar-card">
        <b>👤 {st.session_state.current_user}</b><br>
        <small>Status: Online</small>
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕ New Chat", use_container_width=True):
        cid = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state.current_chat_id = cid
        st.session_state.all_chats[cid] = {
            "name": f"Chat {len(st.session_state.all_chats)+1}",
            "messages": [],
            "created_at": datetime.now().strftime("%d %b %Y %H:%M")
        }
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("### 💬 Chats")
    for cid, chat in st.session_state.all_chats.items():
        if st.button(chat["name"], key=cid):
            st.session_state.current_chat_id = cid
            st.session_state.chat_history = chat["messages"]
            st.rerun()

    role = st.selectbox(
        "Assistant Role",
        ["Assistant", "Tutor", "Coding Assistant", "Career Mentor"]
    )

    st.markdown("### 📤 Export")
    if st.button("Export PDF"):
        export_pdf(Memory().get_history())
    if st.button("Export TXT"):
        export_text(Memory().get_history())

    if st.button("Logout", type="primary"):
        st.session_state.clear()
        st.rerun()


# ==========================
# MAIN CHAT
# ==========================
st.markdown(f"<div class='title'>🤖 JARVIS – {role}</div>", unsafe_allow_html=True)

settings = APIKey()
engine = GeminiEngine(settings.load_api_key())
memory = Memory()
prompt_controller = PromptController(role)
assistant = JarvisAssistant(
    engine=engine,
    prompt_controller=prompt_controller,
    memory=memory
)


chat_box = st.container()
with chat_box:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>{msg['message']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>{msg['message']}</div>", unsafe_allow_html=True)


uploaded_file = st.file_uploader("Upload text file (optional)", type=["txt"])
file_text = uploaded_file.read().decode("utf-8") if uploaded_file else ""


col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.chat_input("Type your message…")
with col2:
    if st.button("🎤"):
        user_input = listen()

if user_input and not st.session_state.is_processing:
    st.session_state.is_processing = True

    if file_text:
        user_input += f"\n\n[File]\n{file_text}"

    # USER MESSAGE
    st.session_state.chat_history.append({
        "role": "user",
        "message": user_input
    })

    # AI RESPONSE
    answer = assistant.respond(user_input)

    st.session_state.chat_history.append({
        "role": "assistant",
        "message": answer
    })

    st.session_state.all_chats[
        st.session_state.current_chat_id
    ]["messages"] = st.session_state.chat_history

    st.session_state.is_processing = False
    st.rerun()

