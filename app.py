import os
import json
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from google.cloud import speech_v1 as speech
from google.oauth2 import service_account

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load credentials from environment variable
credentials_info = json.loads(os.environ["GOOGLE_CLOUD_KEY"])
credentials = service_account.Credentials.from_service_account_info(credentials_info)
client = speech.SpeechClient(credentials=credentials)

@app.route('/')
def home():
    return "Flask + Google Speech API is working!"

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400

    audio = speech.RecognitionAudio(content=audio_file.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)
    text = " ".join([result.alternatives[0].transcript for result in response.results])
    return jsonify({"transcript": text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
