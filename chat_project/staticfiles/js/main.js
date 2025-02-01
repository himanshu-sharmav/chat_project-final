document.addEventListener('DOMContentLoaded', function() {
    // Toggle left menu
    const toggleButton = document.getElementById('toggle-menu');
    const leftMenu = document.getElementById('left-menu');
    
    if (toggleButton && leftMenu) {
        toggleButton.addEventListener('click', function() {
            leftMenu.classList.toggle('collapsed');
        });
    }

    // WebSocket connection for chat
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        const roomName = chatContainer.getAttribute('data-room');
        const chatSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
        );

        const chatMessages = document.querySelector('#chat-messages');
        
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            
            if (data.type === 'clear_messages') {
                chatMessages.innerHTML = '';
                return;
            }
            
            if (data.type === 'chat_message') {
                appendMessage(data.message, data.sender, data.timestamp);
            }
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        const messageInput = document.querySelector('#chat-message-input');
        const messageSubmit = document.querySelector('#chat-message-submit');

        if (messageInput && messageSubmit) {
            messageInput.focus();
            messageInput.onkeyup = function(e) {
                if (e.keyCode === 13 && !e.shiftKey) {  // enter key without shift
                    e.preventDefault();
                    messageSubmit.click();
                }
            };

            messageSubmit.onclick = function(e) {
                const message = messageInput.value.trim();
                if (message) {
                    chatSocket.send(JSON.stringify({
                        'type': 'chat_message',
                        'message': message,
                        'receiver': roomName
                    }));
                    messageInput.value = '';
                }
            };
        }
    }
});

function appendMessage(message, sender, timestamp) {
    const chatMessages = document.querySelector('#chat-messages');
    if (chatMessages) {
        const messageElement = document.createElement('div');
        const currentUser = document.querySelector('.navbar-nav .nav-link').textContent.replace('Welcome, ', '').trim();
        
        messageElement.classList.add('message');
        messageElement.classList.add(sender === currentUser ? 'sent' : 'received');
        
        const time = timestamp ? new Date(timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();
        messageElement.innerHTML = `
            <div class="message-content">
                <strong>${sender}:</strong> ${message}
                <small class="message-time">${time}</small>
            </div>
        `;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}