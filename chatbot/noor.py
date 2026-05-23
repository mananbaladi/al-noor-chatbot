import gspread
import datetime
import streamlit as st
from google.oauth2.service_account import Credentials
from chatbot.gemini_client import ask_gemini, ask_gemini_stream
from chatbot.prompts import REFRAME_SYSTEM_PROMPT, FOLLOW_UP_SYSTEM_PROMPT

SHEET_ID = "1iE7ZqGcA36B_T269ryDnsBJAHR0g2lBL4WRx-nNN7uY"

def log_to_sheets(question):
    try:
        scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([now, question])
    except Exception as e:
        print(f"Sheets error: {e}")

class NoorChatbot:
    def __init__(self):
        self.conversation_count = 0

    def reframe_stream(self, user_message: str):
        log_to_sheets(user_message)
        self.conversation_count += 1
        system = REFRAME_SYSTEM_PROMPT if self.conversation_count == 1 else FOLLOW_UP_SYSTEM_PROMPT
        full_prompt = f"{system}\n\nUser: {user_message}"
        yield from ask_gemini_stream(full_prompt)

    def reset(self):
        self.conversation_count = 0