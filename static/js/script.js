let chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');

function renderChat() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
    chatHistory.forEach(msg => {
        const msgDiv = document.createElement('div');
        msgDiv.className = msg.role === 'user' ? 'user-message' : 'bot-message';
        msgDiv.textContent = msg.text;
        chatBox.appendChild(msgDiv);
    });
    chatBox.scrollTop = chatBox.scrollHeight;
    renderHistory();
}

function renderHistory() {
    const historyList = document.getElementById('history');
    historyList.innerHTML = '';
    chatHistory.forEach((msg, index) => {
        if (msg.role === 'user') {
            const li = document.createElement('li');
            li.textContent = msg.text.slice(0, 30) + (msg.text.length > 30 ? '...' : '');
            li.onclick = () => {
                alert(`User: ${msg.text}\nBot: ${chatHistory[index + 1]?.text || ''}`);
            };
            historyList.appendChild(li);
        }
    });
}

function saveHistory() {
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

function toggleDarkMode() {
    document.body.classList.toggle('dark');
}

function startVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();
    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('user-input').value = transcript;
    };

    recognition.onerror = function (event) {
        alert('Voice recognition error: ' + event.error);
    };
}

async function sendMessage() {
    const inputEl = document.getElementById('user-input');
    const userInput = inputEl.value.trim();
    if (!userInput) return;

    chatHistory.push({ role: 'user', text: userInput });
    renderChat();
    inputEl.value = '';
    saveHistory();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput })
        });

        const data = await response.json();
        chatHistory.push({ role: 'bot', text: data.response });
        saveHistory();
        renderChat();
    } catch (err) {
        chatHistory.push({ role: 'bot', text: 'Error: Could not reach server.' });
        saveHistory();
        renderChat();
    }
}

// Send on Enter (Shift+Enter for newline)
document.getElementById('user-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Load chat on startup
renderChat();
