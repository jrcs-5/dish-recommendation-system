document.getElementById('chat-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const messageInput = document.getElementById('user-message');
    const userMessage = messageInput.value;

    if (!userMessage.trim()) return; // Evitar mensajes vacíos

    // Agregar mensaje del usuario al contenedor de chat
    addMessage(userMessage, 'user');

    // Limpiar el campo de entrada
    messageInput.value = "";

    // Mostrar indicador de "escribiendo..."
    const typingIndicator = addMessage('Escribiendo...', 'bot');

    // Enviar mensaje al backend
    try {
        const response = await fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();

        // Eliminar indicador de "escribiendo..."
        typingIndicator.remove();

        // Agregar respuesta del bot al contenedor de chat
        addMessage(data.response, 'bot');
    } catch (error) {
        typingIndicator.remove();
        addMessage('Error al comunicarse con el servidor: ' + error.message, 'bot');
    }
});

function addMessage(text, sender) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerText = text;
    chatContainer.appendChild(messageDiv);

    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageDiv;
}