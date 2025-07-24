const socket = io();
const output = document.getElementById('output');
let mediaRecorder, audioChunks = [];

document.getElementById('start').onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start(1000);  // every second

    mediaRecorder.ondataavailable = (e) => {
        socket.emit('audio', e.data);
    };
};

document.getElementById('stop').onclick = () => {
    if (mediaRecorder) mediaRecorder.stop();
};

socket.on('transcript', (data) => {
    output.innerHTML += "<br>👉 " + data;
});
