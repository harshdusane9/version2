from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from google.cloud import speech
import base64
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure Google Speech client
speech_client = speech.SpeechClient()

STREAMING_LIMIT = 240000  # max streaming duration in ms (4 min)

# Audio config for Google streaming recognition
streaming_config = speech.StreamingRecognitionConfig(
    config=speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        max_alternatives=1,
    ),
    interim_results=True,
)

@app.route("/")
def index():
    return render_template("index.html")

def generate_requests(audio_generator):
    for content in audio_generator:
        yield speech.StreamingRecognizeRequest(audio_content=content)

@socketio.on("startStream")
def start_stream():
    print("Stream started")

@socketio.on("endStream")
def end_stream():
    print("Stream ended")

@socketio.on("audio")
def audio(data):
    # data is base64 audio chunk from client
    audio_content = base64.b64decode(data)
    requests = generate_requests([audio_content])

    responses = speech_client.streaming_recognize(streaming_config, requests)

    # Because streaming_recognize yields multiple results,
    # but we are sending one chunk at a time, we only take first result here.
    try:
        for response in responses:
            for result in response.results:
                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                emit("transcript", {"transcript": transcript, "is_final": is_final})
                break
            break
    except Exception as e:
        print("Error in speech recognition:", e)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
