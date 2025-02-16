import os
import requests
from deepgram import Deepgram
import google.generativeai as genai

# API Keys
DEEPGRAM_API_KEY = 'your_deepgram_api_key'
GEMINI_API_KEY = 'your_gemini_api_key'

# Transcribe audio using Deepgram
def transcribe_audio(file_path):
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    with open(file_path, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = deepgram.transcription.sync_prerecorded(source, {'smart_format': True})
        return response['results']['channels'][0]['alternatives'][0]['transcript']

# Ask Gemini for a response
def ask_gemini(question):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

# Convert text to speech using Google TTS
def text_to_speech(text, output_path):
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl=en&client=tw-ob"
    response = requests.get(tts_url)
    with open(output_path, 'wb') as f:
        f.write(response.content)

# Main function
if __name__ == "__main__":
    audio_file = 'audio.wav'  # Audio file uploaded by ESP32
    transcribed_text = transcribe_audio(audio_file)
    gemini_response = ask_gemini(transcribed_text)
    text_to_speech(gemini_response, 'response.mp3')  # Save response as audio
