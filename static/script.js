document.getElementById("recordBtn").addEventListener("click", () => {
    fetch("/speech-to-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ audioData: "Sample Audio Data" })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = data.text;
    })
    .catch(err => console.error(err));
});
