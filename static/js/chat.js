// Initialize the event source for streaming responses
const eventSource = new EventSource('/stream');

eventSource.onmessage = function(event) {
    const message = event.data;
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p>${message}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
};

// Save the title of the conversation
function saveTitle() {
    const title = document.getElementById("title-input").value;
    fetch('/save_title', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: title })
    })
    .then(response => response.json())
    .then(data => console.log('Title saved:', data))
    .catch(error => console.error('Error saving title:', error));
}

// Clear the conversation chat box
function clearConversation() {
    document.getElementById("chat-box").innerHTML = '';
}
