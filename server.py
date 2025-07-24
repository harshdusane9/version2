from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from google.cloud import speech_v1 as speech
import os
import io

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Path to your Google credentials (make sure it's on Render or local path for testing)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud.json"
client = speech.SpeechClient()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio')
def handle_audio(audio_data):
    audio_bytes = io.BytesIO(audio_data)
    content = audio_bytes.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True
    )
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        transcript = result.alternatives[0].transcript
        emit('transcript', transcript)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
