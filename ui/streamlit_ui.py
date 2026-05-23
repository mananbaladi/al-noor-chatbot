"""
streamlit_ui.py
Al-Noor - Islamic Positive Reframing Chatbot
Clean centered design matching the HTML version.
"""

import streamlit as st
from chatbot.noor import NoorChatbot
from chatbot.gemini_client import ask_gemini_stream
from chatbot.prompts import REFRAME_SYSTEM_PROMPT, FOLLOW_UP_SYSTEM_PROMPT


def configure_page():
    st.set_page_config(
        page_title="Al-Noor — Positive Reframing Chatbot",
        page_icon="🌙",
        layout="centered",
        initial_sidebar_state="collapsed",
    )


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

    /* Hide Streamlit defaults */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none; }

    /* Full dark background */
    .stApp {
        background: #0f1419 !important;
        font-family: 'DM Sans', sans-serif;
    }

    /* Main container centered */
    .block-container {
        max-width: 780px !important;
        padding: 0 20px 100px 20px !important;
    }

    /* Header bar */
    .top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 0 12px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0;
    }
    .top-bar-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .top-bar-logo {
        width: 38px; height: 38px;
        border-radius: 50%;
        background: rgba(201,168,76,0.15);
        border: 1.5px solid #c9a84c;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
        line-height: 1;
    }
    .top-bar-title { font-size: 17px; font-weight: 500; color: #e8cc7a; }
    .top-bar-sub { font-size: 12px; color: #6b8899; margin-top: 1px; }
    .status { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #4ecdc4; }
    .dot { width: 6px; height: 6px; border-radius: 50%; background: #4ecdc4; }

    /* Welcome screen */
    .welcome-wrap {
        text-align: center;
        padding: 40px 20px 20px;
    }
    .bismillah {
        font-family: 'Amiri', serif;
        font-size: 26px;
        color: #c9a84c;
        direction: rtl;
        margin-bottom: 20px;
    }
    .moon-icon { font-size: 52px; margin-bottom: 10px; display: block; }
    .welcome-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 32px;
        font-weight: 500;
        color: #c9a84c;
        margin-bottom: 14px;
    }
    .welcome-text {
        font-size: 15px;
        color: #8a9bb0;
        line-height: 1.7;
        max-width: 480px;
        margin: 0 auto 6px;
    }
    .powered {
        font-size: 12px;
        color: #4d5e72;
        margin-top: 6px;
    }

    /* Chips row */
    .chips-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin: 20px auto 10px;
        max-width: 560px;
    }

    /* Streamlit buttons as chips */
    .stButton > button {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #8a9bb0 !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        padding: 6px 16px !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s !important;
        white-space: nowrap !important;
    }
    .stButton > button:hover {
        border-color: #c9a84c !important;
        color: #e8cc7a !important;
        background: rgba(201,168,76,0.08) !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 4px 0 !important;
    }

    /* User bubble */
    [data-testid="stChatMessage"][data-testid*="user"] .stMarkdown,
    .user-bubble {
        background: rgba(30,58,47,0.6) !important;
        border: 1px solid rgba(78,205,196,0.15) !important;
        border-radius: 14px !important;
        border-top-right-radius: 4px !important;
        padding: 12px 16px !important;
        color: #e8e8e0 !important;
    }

    /* AI bubble */
    .stChatMessage .stMarkdown p { color: #d0d8e4; line-height: 1.75; }
    .stChatMessage .stMarkdown strong { color: #e8cc7a; }

    /* Verse styling */
    .verse-box {
        background: rgba(201,168,76,0.07);
        border: 1px solid rgba(201,168,76,0.2);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 10px 0;
    }
    .arabic {
        font-family: 'Amiri', serif;
        font-size: 20px;
        color: #e8cc7a;
        direction: rtl;
        text-align: right;
        line-height: 2.2;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background: #1a2130 !important;
        border: 1px solid rgba(201,168,76,0.25) !important;
        border-radius: 14px !important;
    }
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #e8e8e0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: #4d5e72 !important; }
    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(201,168,76,0.5) !important;
    }

    /* Bottom hint */
    .bottom-hint {
        text-align: center;
        font-size: 11px;
        color: #4d5e72;
        margin-top: 6px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }

    /* Hide avatar area padding */
    [data-testid="stChatMessageAvatarAssistant"],
    [data-testid="stChatMessageAvatarUser"] {
        width: 30px !important;
        height: 30px !important;
    }

    p { color: #d0d8e4; }
    </style>
    """, unsafe_allow_html=True)


def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "noor" not in st.session_state:
        st.session_state.noor = NoorChatbot()
    if "msg_count" not in st.session_state:
        st.session_state.msg_count = 0


def render_header():
    st.markdown("""
    <div class="top-bar">
        <div class="top-bar-left">
            <div class="top-bar-logo">☽</div>
            <div>
                <div class="top-bar-title">Al-Noor</div>
                <div class="top-bar-sub">Positive Reframing · Quranic Wisdom</div>
            </div>
        </div>
        <div class="status">
            <div class="dot"></div>
            Online
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_welcome():
    st.markdown("""
    <div class="welcome-wrap">
        <div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
        <span class="moon-icon">🌙</span>
        <div class="welcome-title">Assalamu Alaikum</div>
        <div class="welcome-text">
            Share any negative thought, worry, or struggle. I will gently reframe
            it into hope and light, and share a Quranic verse that speaks to your heart.
        </div>
        <div class="powered">Powered by Manan</div>
    </div>
    """, unsafe_allow_html=True)

    # Chips in 2 columns 3 rows like HTML design
    prompts = [
        "I feel like a failure",
        "I'm so stressed about the future",
        "Nobody cares about me",
        "I've made too many mistakes",
        "Life feels hopeless",
        "I'm always anxious",
    ]

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    for row in range(3):
        c1, c2 = st.columns(2)
        with c1:
            i = row * 2
            if st.button(prompts[i], key=f"chip_{i}", use_container_width=True):
                st.session_state["quick_prompt"] = prompts[i]
                st.rerun()
        with c2:
            i = row * 2 + 1
            if st.button(prompts[i], key=f"chip_{i}", use_container_width=True):
                st.session_state["quick_prompt"] = prompts[i]
                st.rerun()
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


def render_chat_history():
    for msg in st.session_state.messages:
        avatar = "🌙" if msg["role"] == "assistant" else "🧑"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])


def get_streaming_response(user_input: str) -> str:
    is_first = st.session_state.msg_count == 1
    system = REFRAME_SYSTEM_PROMPT if is_first else FOLLOW_UP_SYSTEM_PROMPT
    full_prompt = f"{system}\n\nUser: {user_input}"
    with st.chat_message("assistant", avatar="🌙"):
        full_response = st.write_stream(ask_gemini_stream(full_prompt))
    return full_response


def handle_input():
    quick_prompt = st.session_state.pop("quick_prompt", None)
    user_input = st.chat_input("Share what's on your heart…") or quick_prompt

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        st.session_state.msg_count += 1
        full_response = get_streaming_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


def run_app():
    configure_page()
    inject_css()
    init_session()
    render_header()

    if len(st.session_state.messages) == 0:
        render_welcome()
    else:
        render_chat_history()

    handle_input()

    st.markdown("""
    <div class="bottom-hint">
        Everything shared here is between you and Al-Noor · Powered by Manan
    </div>
    """, unsafe_allow_html=True)