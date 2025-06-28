import os
import requests

OPENAI_API_KEY = ""

def transcribe(path: str) -> str:
    """Send WAV at `path` to OpenAI Whisper API and return transcript."""
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    with open(path, "rb") as f:
        resp = requests.post(url, headers=headers, files={"file": f}, data={"model": "whisper-1"})
    resp.raise_for_status()
    return resp.json()["text"]

def chat_reply(prompt: str, history: list) -> str:
    """Send `prompt` + `history` to ChatCompletions, return reply."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = {
        "role": "system",
        "content": (
            "You are a helpful assistant, you give short responses, "
            "use words that are easy to pronounce, "
        )
    }
    
    messages = [system_prompt] + history + [{"role": "user", "content": prompt}]
    payload = {"model": "gpt-4o", "messages": messages}
    
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def synthesize(text: str, outpath: str):
    """Call TTS endpoint, save audio to `outpath`."""
    url = "https://api.openai.com/v1/audio/speech"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {"model": "tts-1", "voice": "alloy", "input": text}
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    with open(outpath, "wb") as f:
        f.write(resp.content)
