const API_URL = 'http://127.0.0.1:8000';
let sessionId = localStorage.getItem('athena_session_id') || null;
let briefingCollapsed = false;

// ── Init ─────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    setGreeting();
    setDate();
    loadBriefing();
});

function setGreeting() {
    const hour = new Date().getHours();
    let greeting = 'Good evening';
    if (hour < 12) greeting = 'Good morning';
    else if (hour < 17) greeting = 'Good afternoon';
    document.getElementById('headerGreeting').textContent = greeting;
}

function setDate() {
    const now = new Date();
    const options = { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' };
    document.getElementById('headerDate').textContent = now.toLocaleDateString('en-US', options);
}

// ── Briefing ─────────────────────────────────────────

async function loadBriefing() {
    const content = document.getElementById('briefingContent');
    content.innerHTML = '<div class="briefing-loading">Loading your briefing<span class="dots"><span>.</span><span>.</span><span>.</span></span></div>';

    try {
        const response = await fetch(`${API_URL}/briefing`);
        const data = await response.json();
        content.innerHTML = formatBriefingText(data.briefing);
        updateStats(data);
    } catch (error) {
        content.innerHTML = '<span style="color: var(--text-muted); font-style: italic;">Unable to load briefing — is the server running?</span>';
    }
}

function formatBriefingText(text) {
    // Convert **bold** and basic formatting
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
}

function updateStats(data) {
    // These will be populated when briefing data includes stats
    // For now show placeholder
    document.getElementById('statTasks').textContent = '◈  tasks';
    document.getElementById('statEvents').textContent = '◷  events';
    document.getElementById('statGoals').textContent = '◎  goals';
}

function toggleBriefing() {
    const panel = document.getElementById('briefingPanel');
    const btn = document.getElementById('collapseBtn');
    briefingCollapsed = !briefingCollapsed;
    panel.classList.toggle('collapsed', briefingCollapsed);
    btn.textContent = briefingCollapsed ? '+' : '−';
}

// ── Theme ─────────────────────────────────────────────

function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    html.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
    localStorage.setItem('athena_theme', current === 'dark' ? 'light' : 'dark');
}

// Restore saved theme
const savedTheme = localStorage.getItem('athena_theme');
if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme);

// ── Chat ──────────────────────────────────────────────

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    if (!message) return;

    input.value = '';
    autoResize(input);

    // Hide welcome
    const welcome = document.getElementById('welcomeMsg');
    if (welcome) welcome.style.display = 'none';

    // Hide briefing after first message
    const briefingPanel = document.getElementById('briefingPanel');
    if (briefingPanel) {
        briefingPanel.style.transition = 'opacity 0.4s ease, max-height 0.4s ease';
        briefingPanel.style.opacity = '0';
        setTimeout(() => briefingPanel.style.display = 'none', 400);
    }

    addMessage(message, 'user');

    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;

    // Typing indicator
    const typingId = 'typing-' + Date.now();
    addTypingIndicator(typingId);

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        const data = await response.json();
        sessionId = data.session_id;
        localStorage.setItem('athena_session_id', sessionId);

        removeTypingIndicator(typingId);
        addMessage(data.reply, 'athena');

    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('Unable to reach Athena — is the server running?', 'error');
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

function addMessage(text, sender) {
    const messages = document.getElementById('messages');

    const row = document.createElement('div');
    row.classList.add('message-row', sender);

    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble');
    bubble.innerHTML = formatMessage(text);

    row.appendChild(bubble);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
}

function formatMessage(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

function addTypingIndicator(id) {
    const messages = document.getElementById('messages');
    const row = document.createElement('div');
    row.classList.add('message-row', 'athena');
    row.id = id;
    row.innerHTML = `<div class="spinner"></div>`;
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ── Input helpers ─────────────────────────────────────

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 140) + 'px';
}

// ── New chat ──────────────────────────────────────────

function newChat() {
    sessionId = null;
    localStorage.removeItem('athena_session_id');

    // Restore briefing panel
    const briefingPanel = document.getElementById('briefingPanel');
    if (briefingPanel) {
        briefingPanel.style.display = '';
        briefingPanel.style.opacity = '1';
    }

    // Reload briefing content
    loadBriefing();

    const messages = document.getElementById('messages');
    messages.innerHTML = `
        <div class="welcome" id="welcomeMsg">
            <div class="welcome-glyph">
                <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" width="48" height="48">
                    <ellipse cx="24" cy="28" rx="15" ry="16" stroke="currentColor" stroke-width="1.2"/>
                    <circle cx="17" cy="24" r="5" stroke="currentColor" stroke-width="1.2"/>
                    <circle cx="31" cy="24" r="5" stroke="currentColor" stroke-width="1.2"/>
                    <circle cx="17" cy="24" r="1.8" fill="currentColor"/>
                    <circle cx="31" cy="24" r="1.8" fill="currentColor"/>
                    <path d="M19 13 C19 9 24 7 24 7 C24 7 29 9 29 13" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    <path d="M14 14 L10 10" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    <path d="M34 14 L38 10" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    <path d="M20 33 Q24 37 28 33" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
            </div>
            <p class="welcome-primary">How can I help you?</p>
            <p class="welcome-secondary">Ask anything, or review your briefing above</p>
        </div>`;
}
