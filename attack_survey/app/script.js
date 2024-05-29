        // JavaScript code to handle the sending of messages
        document.getElementById('send-btn').addEventListener('click', function() {
            const userInput = document.getElementById('user-input').value;
    
            // Display user input as a new message
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'message user-message';
            userMessageDiv.textContent = `User: ${userInput}`;
            document.querySelector('.chat-box').appendChild(userMessageDiv);
    
            // Clear the input field
            document.getElementById('user-input').value = '';
    
            // Make the API request and handle the response
            fetch('http://127.0.0.1:8080/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userInput })
            })
            .then(response => response.json())
            .then(data => {
                // Display the assistant's response as a new message
                const assistantMessageDiv = document.createElement('div');
                assistantMessageDiv.className = 'message assistant-message';
                assistantMessageDiv.textContent = `Assistant: ${data.response}`;
                document.querySelector('.chat-box').appendChild(assistantMessageDiv);
            })
            .catch(error => {
                console.error('Error sending POST request:', error);
            });
        });