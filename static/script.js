document.addEventListener('DOMContentLoaded', function () {
    const chatButton = document.getElementById("start-chat-btn");
    if (chatButton) {
        chatButton.addEventListener('click', function () {
            window.location.href = "/chat";
        });
    }


    const chatForm = document.getElementById("chat-form");
    chatForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const userMessage = document.getElementById("user-message").value;
        const portions = document.getElementById("portion-quantity").value;
        const recipeType = document.querySelector('input[name="recipe-type"]:checked').value;

        const data = {
            message: userMessage,
            portions: portions,
            type: recipeType
        };
        try {
            const response = await fetch("/chat/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const markdownContent = await response.text();
            if (response.ok) {
                addMessage(markdownContent);
            } else {
                console.error("Error en la respuesta del servidor:", markdownContent);
                alert("Error: " + markdownContent); 
            }
        } catch (error) {
            console.error("Error al enviar la solicitud:", error);
            alert("Hubo un problema al enviar la solicitud.");
        }
    });
});

function addMessage(markdownContent) {
    const chatContainer = document.getElementById('message-container');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.innerHTML = marked.parse(markdownContent.trim());
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageDiv;
}


document.getElementById("back-btn").addEventListener("click", () => {
    window.location.href = "/";
});





async function fetchDishes() {
    try {
        const response = await fetch("/dishes");
        if (!response.ok) {
            throw new Error("Error al obtener las recetas.");
        }
        const data = await response.json();
        const dishes = data.dishes;

        const dishContainer = document.getElementById("dish-container");
        dishContainer.innerHTML = "";

        if (dishes.length === 0) {
            dishContainer.innerHTML = "<p>No hay recetas disponibles.</p>";
            return;
        }
        dishes.forEach(dish => {
            const dishElement = document.createElement("div");
            dishElement.className = "dish-item";
            dishElement.textContent = dish;
            dishContainer.appendChild(dishElement);
        });
    } catch (error) {
        console.error("Error:", error);
        const dishContainer = document.getElementById("dish-container");
        dishContainer.innerHTML = "<p>Error al cargar las recetas.</p>";
    }
}

document.addEventListener("DOMContentLoaded", fetchDishes);