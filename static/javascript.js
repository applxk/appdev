function toggleChat() {
    var chatContainer = document.getElementById('chat-container');
    chatContainer.classList.toggle('visible');

    if (!chatContainer.classList.contains('visible')) {
        $('#chat-body').empty();
    }
}

function sendMessage() {
    var userInput = $('input[name="user_message"]').val();

    if (userInput) {
        var chatBody = $('#chat-body');
        var userMessage = '<div class="message user-message"><span class="user-icon">👤</span>' + userInput + '</div>';
        chatBody.append(userMessage);

        $.ajax({
            type: 'POST',
            url: '/chat',
            data: { user_message: userInput },
            success: function (response) {
                if (response) {
                    var botMessage = '<div class="message bot-message"><span class="bot-icon">🤖</span>' + response + '</div>';
                    chatBody.append(botMessage);
                }
            },
            error: function (error) {
                console.error('Error sending message:', error);
            }
        });

        $('input[name="user_message"]').val('');
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
}