"""
gemini_client.py
Uses GitHub Models API (GPT-5) - Free with GitHub Education.
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = "https://models.inference.ai.azure.com/chat/completions"
MODEL = "gpt-4o"  # works reliably; change to "openai-gpt-5" if available


def ask_gemini(prompt: str, system_prompt: str = "") -> str:
    """Send prompt to GitHub Models and return full response."""
    api_key = os.getenv("GITHUB_TOKEN")
    if not api_key:
        return "⚠️ GITHUB_TOKEN not found in .env file."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    body = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.8,
    }

    try:
        resp = requests.post(GITHUB_API_URL, headers=headers, json=body, timeout=30)
        data = resp.json()
        if resp.status_code == 200:
            return data["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Error: {data.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"⚠️ Connection Error: {e}"


def ask_gemini_stream(prompt: str, system_prompt: str = ""):
    """Stream response from GitHub Models word by word."""
    api_key = os.getenv("GITHUB_TOKEN")
    if not api_key:
        yield "⚠️ GITHUB_TOKEN not found in .env file."
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    body = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.8,
        "stream": True,
    }

    try:
        with requests.post(
            GITHUB_API_URL, headers=headers, json=body, stream=True, timeout=60
        ) as resp:
            for line in resp.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data:"):
                        chunk = line[5:].strip()
                        if chunk == "[DONE]":
                            return
                        try:
                            data = json.loads(chunk)
                            delta = data["choices"][0]["delta"]
                            text = delta.get("content", "")
                            if text:
                                yield text
                        except Exception:
                            continue
    except Exception as e:
        yield f"⚠️ Error: {e}"
