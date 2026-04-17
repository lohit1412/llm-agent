const API_URL = 'http://127.0.0.1:8000';
let sessionId = localStorage.getItem('athena_session_id') || null; // ← changed

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if(!message) return;

    input.value = '';
    addMessage(message, 'user');

    const welcome = document.querySelector('.welcome');
    if (welcome) welcome.style.display = 'none';

    const sendBtn = document.querySelector('.send-btn');
    sendBtn.disabled = true;

    const loadingId = 'loading-' + Date.now();
    const loadingBubble = document.createElement('div');
    loadingBubble.classList.add('message', 'athena');
    loadingBubble.id = loadingId;
    loadingBubble.textContent = '...';
    document.getElementById('messages').appendChild(loadingBubble);

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                session_id: sessionId  // ← changed
            })
        });

        const data = await response.json();
        sessionId = data.session_id;  // ← changed
        localStorage.setItem('athena_session_id', sessionId);  // ← added
        document.getElementById(loadingId).remove();
        addMessage(data.reply, 'athena');
    } catch (error) {
        document.getElementById(loadingId).remove();
        addMessage('Error connecting to Athena. is the server running?', 'error');
    } finally {
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
    localStorage.removeItem('athena_session_id');  // ← added
    const messages = document.getElementById('messages');
    messages.innerHTML = '<div class="welcome"><p>How can I help you today?</p></div>';
}