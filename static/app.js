// Global variables
let socket;
let currentSessionId = null;
let isAutomationRunning = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeParticles();
    initializeSocket();
    updateUI();
});

// Create animated background particles
function initializeParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random position and animation delay
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
        
        particlesContainer.appendChild(particle);
    }
}

// Initialize Socket.IO connection
function initializeSocket() {
    socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to server');
        addStatusMessage('Connected to server', 'success');
        updateStatusIndicator('connected');
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        addStatusMessage('Disconnected from server', 'error');
        updateStatusIndicator('disconnected');
    });
    
    socket.on('status_update', function(data) {
        addStatusMessage(data.message, data.type);
    });
    
    socket.on('automation_ready', function(data) {
        addStatusMessage(data.message, 'success');
        enableChatInterface();
    });
    
    socket.on('automation_error', function(data) {
        addStatusMessage('Automation error: ' + data.error, 'error');
        resetAutomation();
    });
    
    socket.on('message_response', function(data) {
        addChatMessage(data.question, 'user');
        addChatMessage(data.response, 'bot');
        enableSendButton();
    });
    
    socket.on('message_error', function(data) {
        addStatusMessage('Message error: ' + data.error, 'error');
        enableSendButton();
    });
}

// Start automation
async function startAutomation() {
    try {
        updateStatusIndicator('loading');
        addStatusMessage('Starting automation...', 'info');
        
        const startBtn = document.getElementById('startBtn');
        startBtn.disabled = true;
        startBtn.innerHTML = '<div class="loading"></div> Starting...';
        
        const response = await fetch('/api/start_automation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentSessionId = data.session_id;
            isAutomationRunning = true;
            
            // Join the session room
            socket.emit('join_session', { session_id: currentSessionId });
            
            addStatusMessage(data.message, 'success');
            updateUI();
        } else {
            addStatusMessage('Failed to start automation: ' + data.error, 'error');
            resetAutomation();
        }
        
    } catch (error) {
        addStatusMessage('Error starting automation: ' + error.message, 'error');
        resetAutomation();
    }
}

// Stop automation
async function stopAutomation() {
    try {
        addStatusMessage('Stopping automation...', 'info');
        
        const response = await fetch('/api/stop_automation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addStatusMessage(data.message, 'success');
        } else {
            addStatusMessage('Failed to stop automation: ' + data.error, 'error');
        }
        
        resetAutomation();
        
    } catch (error) {
        addStatusMessage('Error stopping automation: ' + error.message, 'error');
        resetAutomation();
    }
}

// Send message to ChatGPT
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) {
        addStatusMessage('Please enter a message', 'warning');
        return;
    }
    
    if (!currentSessionId) {
        addStatusMessage('Please start automation first', 'warning');
        return;
    }
    
    try {
        // Disable send button and show loading
        disableSendButton();
        
        // Clear input
        messageInput.value = '';
        
        const response = await fetch('/api/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addStatusMessage(data.message, 'info');
        } else {
            addStatusMessage('Failed to send message: ' + data.error, 'error');
            enableSendButton();
        }
        
    } catch (error) {
        addStatusMessage('Error sending message: ' + error.message, 'error');
        enableSendButton();
    }
}

// Handle Enter key press in message input
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Add status message
function addStatusMessage(message, type) {
    const statusMessages = document.getElementById('statusMessages');
    const messageElement = document.createElement('div');
    messageElement.className = `status-message ${type}`;
    messageElement.textContent = message;
    
    statusMessages.appendChild(messageElement);
    statusMessages.scrollTop = statusMessages.scrollHeight;
    
    // Remove old messages if too many
    const messages = statusMessages.children;
    if (messages.length > 10) {
        statusMessages.removeChild(messages[0]);
    }
}

// Add chat message
function addChatMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Remove empty state if present
    const emptyState = chatMessages.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }
    
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = message;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = new Date().toLocaleTimeString();
    
    messageElement.appendChild(messageContent);
    messageElement.appendChild(messageTime);
    chatMessages.appendChild(messageElement);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Update status indicator
function updateStatusIndicator(status) {
    const indicator = document.getElementById('statusIndicator');
    indicator.className = 'status-indicator';
    
    if (status === 'connected') {
        indicator.classList.add('connected');
    } else if (status === 'loading') {
        indicator.classList.add('loading');
    }
}

// Update UI based on automation state
function updateUI() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    
    if (isAutomationRunning) {
        startBtn.disabled = true;
        startBtn.innerHTML = '<i class="fas fa-check"></i> Running';
        stopBtn.disabled = false;
    } else {
        startBtn.disabled = false;
        startBtn.innerHTML = '<i class="fas fa-play"></i> Start Automation';
        stopBtn.disabled = true;
    }
}

// Enable chat interface
function enableChatInterface() {
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    
    messageInput.disabled = false;
    sendBtn.disabled = false;
    messageInput.focus();
}

// Disable chat interface
function disableChatInterface() {
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    
    messageInput.disabled = true;
    sendBtn.disabled = true;
}

// Disable send button
function disableSendButton() {
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<div class="loading"></div>';
}

// Enable send button
function enableSendButton() {
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = false;
    sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
}

// Reset automation state
function resetAutomation() {
    isAutomationRunning = false;
    currentSessionId = null;
    updateStatusIndicator('disconnected');
    updateUI();
    disableChatInterface();
    
    const startBtn = document.getElementById('startBtn');
    startBtn.disabled = false;
    startBtn.innerHTML = '<i class="fas fa-play"></i> Start Automation';
}

// Add some visual feedback for button clicks
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn') || e.target.classList.contains('send-btn')) {
        // Create ripple effect
        const ripple = document.createElement('span');
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255,255,255,0.6)';
        ripple.style.transform = 'scale(0)';
        ripple.style.animation = 'ripple 0.6s linear';
        ripple.style.left = (e.offsetX - 10) + 'px';
        ripple.style.top = (e.offsetY - 10) + 'px';
        ripple.style.width = '20px';
        ripple.style.height = '20px';
        
        e.target.style.position = 'relative';
        e.target.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
});

// Add ripple animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
