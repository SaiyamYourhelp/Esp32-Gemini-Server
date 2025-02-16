import os
import requests
import json

# API Keys from GitHub Secrets
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Function to transcribe audio using Deepgram
def transcribe_audio(file_path):
    url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true"
    headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}", "Content-Type": "audio/wav"}

    with open(file_path, "rb") as f:
        response = requests.post(url, headers=headers, data=f)

    if response.status_code == 200:
        return response.json()["results"]["channels"][0]["alternatives"][0]["transcript"]
    return None

# Function to get AI response from Gemini
def get_gemini_response(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": question}]}]}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return None

# Function to convert text to speech using Google TTS
def text_to_speech(text, lang="en"):
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={lang}&client=tw-ob"
    response = requests.get(url)

    if response.status_code == 200:
        with open("server/output.mp3", "wb") as f:
            f.write(response.content)
        return "server/output.mp3"
    return None

# Main script execution
if __name__ == "__main__":
    file_path = "audio/latest.wav"

    transcript = transcribe_audio(file_path)
    if transcript:
        print(f"Transcript: {transcript}")
        response_text = get_gemini_response(transcript)
        
        if response_text:
            print(f"Gemini Response: {response_text}")
            tts_audio = text_to_speech(response_text)
            
            if tts_audio:
                print("TTS generated successfully!")
