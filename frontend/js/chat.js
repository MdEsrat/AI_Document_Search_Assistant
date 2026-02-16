// Chat functionality
const API_BASE_URL = '/api';

const chatForm = document.getElementById('chatForm');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');

let isProcessing = false;

// Chat form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (isProcessing) return;
    
    const question = questionInput.value.trim();
    if (!question) return;
    
    // Add user message
    addMessage(question, 'user');
    questionInput.value = '';
    
    // Show loading
    showLoading();
    isProcessing = true;
    sendBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        // Remove loading
        removeLoading();
        
        if (response.ok) {
            addMessage(data.answer, 'assistant', data.sources);
        } else {
            addMessage('Sorry, I encountered an error processing your question. Please try again.', 'assistant');
        }
    } catch (error) {
        console.error('Query error:', error);
        removeLoading();
        addMessage('Sorry, I encountered an error. Please check if documents are uploaded and try again.', 'assistant');
    } finally {
        isProcessing = false;
        sendBtn.disabled = false;
        questionInput.focus();
    }
});

// Add message to chat
function addMessage(text, role, sources = null) {
    // Remove welcome message if it exists
    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const icon = role === 'user' 
        ? '<i class="bi bi-person-circle message-icon"></i>' 
        : '<i class="bi bi-robot message-icon"></i>';
    
    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `
            <div class="sources">
                <strong>Sources:</strong>
                ${sources.map(source => `<div><i class="bi bi-file-earmark-text"></i> ${source}</div>`).join('')}
            </div>
        `;
    }
    
    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="message-bubble">
                ${escapeHtml(text)}
            </div>
            ${icon}
        `;
    } else {
        messageDiv.innerHTML = `
            ${icon}
            <div class="message-bubble">
                ${escapeHtml(text)}
                ${sourcesHtml}
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Show loading indicator
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.id = 'loadingMessage';
    loadingDiv.innerHTML = `
        <i class="bi bi-robot message-icon"></i>
        <div class="loading-spinner">
            <div class="spinner-border spinner-border-sm text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <span>Thinking...</span>
        </div>
    `;
    chatMessages.appendChild(loadingDiv);
    scrollToBottom();
}

// Remove loading indicator
function removeLoading() {
    const loadingMessage = document.getElementById('loadingMessage');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Focus on input when page loads
questionInput.focus();

// Add enter key event (Shift+Enter for new line, Enter to send)
questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});
