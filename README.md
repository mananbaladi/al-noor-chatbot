# 🌙 Noor نور — AI Positive Reframing Chatbot

> *"Indeed, with hardship comes ease."* — Al-Inshirah 94:5

**Noor** is an AI-powered chatbot that transforms negative thoughts into hope and positivity, paired with authentic Quranic verses — built with Python, Streamlit, and Google Gemini AI.

---

## ✨ Features

- 🫂 **Empathetic Acknowledgment** — Never dismisses your feelings
- ✨ **Positive Reframing** — Turns negative thoughts into empowering perspectives
- 📖 **Quranic Verses** — Real, accurate Arabic verses with translation and reference
- 🌿 **Gentle Action Steps** — One practical thing you can do right now
- 📿 **Daily Affirmations** — Islamic affirmations with duas
- 🤲 **Dua Finder** — Get authentic duas for specific situations
- 💬 **Full Conversation** — Remembers the whole chat session
- ⚡ **Streaming Responses** — Word-by-word output like ChatGPT

---

## 📁 Project Structure

```
noor_chatbot/
├── app.py                  # Entry point
├── requirements.txt        # Dependencies
├── .env                    # API key (add your key here)
├── README.md
├── chatbot/
│   ├── __init__.py
│   ├── gemini_client.py    # Gemini API with streaming & retry
│   ├── prompts.py          # System prompts for reframing & verses
│   └── noor.py             # Core chatbot logic (OOP class)
└── ui/
    ├── __init__.py
    └── streamlit_ui.py     # Full Streamlit frontend
```

---

## 🚀 How to Run

### Step 1 — Extract & Navigate
```cmd
cd noor_chatbot
```

### Step 2 — Create Virtual Environment
```cmd
python -m venv venv
```

### Step 3 — Activate (Command Prompt)
```cmd
venv\Scripts\activate.bat
```

### Step 4 — Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 5 — Add API Key
Open `.env` and replace with your actual key:
```
GEMINI_API_KEY=your_actual_key_here
```
Get a free key at: https://aistudio.google.com/app/apikey

### Step 6 — Run
```cmd
streamlit run app.py
```

---

## 🔧 OOP Concepts Used

| Concept | Where Used |
|---------|-----------|
| **Encapsulation** | `NoorChatbot` class hides internal logic |
| **Abstraction** | `ask_gemini()` hides API complexity |
| **Modularity** | Each file has one responsibility |
| **Separation of Concerns** | UI, logic, and prompts are separate layers |

---

## 💡 Troubleshooting

| Error | Fix |
|-------|-----|
| `429 Quota exceeded` | Create a new API key from a different Google account |
| `503 UNAVAILABLE` | Auto-retries 3 times; wait a moment and try again |
| `GEMINI_API_KEY not found` | Check your `.env` file has the key with no spaces |

---

*Powered by Manan · Built with Streamlit & Gemini AI · نور*
