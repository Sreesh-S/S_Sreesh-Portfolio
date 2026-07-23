/* -------------------------------------------------------------
   AI FLOATING CHAT ASSISTANT
   ------------------------------------------------------------- */

(function() {
    const trigger = document.getElementById('ai-trigger');
    const panel = document.getElementById('ai-chat-panel');
    const closeBtn = document.getElementById('ai-close-btn');
    const chatForm = document.getElementById('ai-chat-form');
    const chatInput = document.getElementById('ai-chat-input');
    const chatBody = document.getElementById('ai-chat-body');

    if (!trigger || !panel) return;

    // Toggle Chat Panel
    trigger.addEventListener('click', function(e) {
        e.stopPropagation();
        panel.classList.toggle('hidden');
        if (!panel.classList.contains('hidden')) {
            chatInput.focus();
            scrollToBottom();
        }
    });

    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        panel.classList.add('hidden');
    });

    // Close panel when clicking outside
    document.addEventListener('click', function(e) {
        if (!panel.contains(e.target) && !trigger.contains(e.target)) {
            panel.classList.add('hidden');
        }
    });

    // Handle Form Submit
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        // 1. Append User Message
        appendMessage(text, 'user');
        chatInput.value = '';
        scrollToBottom();

        // Show typing indicator
        const typingId = showTypingIndicator();
        scrollToBottom();

        // 2. Fetch AI Response
        fetch('/ai-assistant/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            removeTypingIndicator(typingId);
            // 3. Append Bot Message with simulated typing
            appendMessage(data.reply, 'bot');
            scrollToBottom();
        })
        .catch(err => {
            removeTypingIndicator(typingId);
            appendMessage("Sorry, I encountered connection trouble. Please try again.", 'bot');
            scrollToBottom();
            console.error(err);
        });
    });

    function appendMessage(content, sender) {
        const bubble = document.createElement('div');
        bubble.className = `chat-message ${sender}-msg`;
        bubble.innerHTML = content; // Allows links and bullet points
        chatBody.appendChild(bubble);
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const bubble = document.createElement('div');
        bubble.id = id;
        bubble.className = 'chat-message bot-msg typing-indicator';
        bubble.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
        
        // Add styling for typing dots if not in main CSS
        const style = document.createElement('style');
        style.innerHTML = `
            .typing-indicator { display: flex; gap: 4px; align-items: center; padding: 12px 16px; }
            .typing-dot { width: 6px; height: 6px; background-color: var(--text-muted); border-radius: 50%; display: inline-block; animation: bounceDot 1.4s infinite ease-in-out both; }
            .typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .typing-dot:nth-child(2) { animation-delay: -0.16s; }
            @keyframes bounceDot {
                0%, 80%, 100% { transform: scale(0); }
                40% { transform: scale(1); }
            }
        `;
        document.head.appendChild(style);
        
        chatBody.appendChild(bubble);
        return id;
    }

    function removeTypingIndicator(id) {
        const indicator = document.getElementById(id);
        if (indicator) indicator.remove();
    }

    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // CSRF Cookie Helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})();
