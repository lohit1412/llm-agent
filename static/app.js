const API_URL = 'http://127.0.0.1:8000';
let sessionId = null;

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if(!message) return;

    // Clear input
    input.value = '';

    // Show user message
    addMessage(message, 'user');

    // Hide welcome message if visible
    const welcome = document.querySelector('.welcome');
    if (welcome) welcome.style.display = 'none';

    // Disable send while waiting
    const sendBtn = document.querySelector('.send-btn');
    sendBtn.disabled = true;

    // Add loading bubble
    const loadingId = 'loading-' + Date.now();
    const loadingBubble = document.createElement('div');
    loadingBubble.classList.add('message', 'athena');
    loadingBubble.id = loadingId;
    loadingBubble.textContent = '...';
    document.getElementById('messages').appendChild(loadingBubble);

    // Send to API
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                sessionId: sessionId
            })
        });

        const data = await response.json();
        sessionId = data.sessionId;
        document.getElementById(loadingId).remove();
        addMessage(data.reply, 'athena');
    } catch (error) {
        addMessage('Error connecting to Athena. is the server running?', 'error');
    } finally {
        // Always re-enable send
        sendBtn.disabled = false;
    }
}

function addMessage(text, sender) {
    const messages = document.getElementById('messages');

    const bubble = document.createElement('div');
    bubble.classList.add('message', sender);
    bubble.textContent = text;

    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function newChat() {
    sessionId = null;
    const messages = document.getElementById('messages');
    messages.innerHTML = ' <div class="welcome"><p>How can I help you today?</p></div>';
}