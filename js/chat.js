document.addEventListener('DOMContentLoaded', () => {
    // --- Chat Elements ---
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send-btn');
    const chatIcon = document.getElementById('chat-icon');
    const expandBtn = document.getElementById('chat-expand-btn');

    // --- State ---
    let isChatOpen = false;
    let isExpanded = false;

    // --- API Endpoint ---
    const API_URL = 'https://rag-backend.onrender.com/chat';

    // --- Functions ---

    // Toggle Chat Window
    function toggleChat() {
        console.log("toggleChat called");
        isChatOpen = !isChatOpen;
        chatWindow.classList.toggle('active');
        chatToggle.classList.toggle('opened');

        // Change icon based on state
        if (isChatOpen) {
            chatIcon.classList.remove('fa-comments');
            chatIcon.classList.add('fa-times');
            chatInput.focus();
        } else {
            chatIcon.classList.remove('fa-times');
            chatIcon.classList.add('fa-comments');
            // Reset expansion when closed
            if (isExpanded) {
                toggleExpand();
            }
        }
    }

    // Toggle Expand Window
    function toggleExpand() {
        isExpanded = !isExpanded;
        chatWindow.classList.toggle('expanded');

        // Update icon
        const icon = expandBtn.querySelector('i');
        if (isExpanded) {
            icon.classList.remove('fa-expand-alt');
            icon.classList.add('fa-compress-alt');
        } else {
            icon.classList.remove('fa-compress-alt');
            icon.classList.add('fa-expand-alt');
        }
    }

    // Add Message to Chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        // Simple formatting
        const formattedText = text.replace(/\n/g, '<br>');
        messageDiv.innerHTML = formattedText;

        chatMessages.appendChild(messageDiv);

        // Auto-scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show Typing Indicator
    function showTyping() {
        removeTyping();

        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.classList.add('message', 'bot', 'typing-indicator');
        typingDiv.style.display = 'flex';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Remove Typing Indicator
    function removeTyping() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    // Send Message to Bot
    async function sendMessage() {
        const userText = chatInput.value.trim();
        if (!userText) return;

        // 1. Add User Message
        addMessage(userText, 'user');
        chatInput.value = '';
        chatInput.disabled = true;

        // 2. Show Typing Indicator
        showTyping();

        try {
            // 3. Send Request to Backend
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userText })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // 4. Remove Typing & Add Bot Response
            removeTyping();
            addMessage(data.response, 'bot');

        } catch (error) {
            console.error('Error:', error);
            removeTyping();
            addMessage("Sorry, I'm having trouble connecting to my brain right now. Please try again later.", 'bot');
        } finally {
            chatInput.disabled = false;
            chatInput.focus();
        }
    }

    // --- Event Listeners ---

    if (chatToggle) {
        chatToggle.addEventListener('click', toggleChat);
    }

    if (expandBtn) {
        expandBtn.addEventListener('click', toggleExpand);
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Handle Suggestions
    document.querySelectorAll('.suggestion-chip').forEach(chip => {
        chip.addEventListener('click', function () {
            chatInput.value = this.textContent;
            sendMessage();
        });
    });
});
