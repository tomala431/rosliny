document.addEventListener("DOMContentLoaded", function () {
    const flowerBox = document.getElementById("flowerBox");

    // Tablica dostępnych obrazków kwiatków
    const flowerImages = [
        '/static/icons/flower1.png',
        '/static/icons/flower2.png',
        '/static/icons/flower3.png'
    ];

    for (let i = 0; i < plantCount; i++) {
        const flower = document.createElement("div");
        flower.classList.add("flower");

        // Losowy wybór obrazka
        const randomIndex = Math.floor(Math.random() * flowerImages.length);
        const selectedImage = flowerImages[randomIndex];

        // Ustawiamy tło na losowy obrazek
        flower.style.backgroundImage = `url('${selectedImage}')`;

        flowerBox.appendChild(flower);
    }

    // Funkcja otwierająca i zamykająca czat
    const chatBox = document.getElementById('liveChat');
    const closeChatButton = document.getElementById('closeChat');
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendMessage');
    const chatMessages = document.getElementById('chatMessages');
    const openChatButton = document.getElementById('openChat');  // Dodaj przycisk otwierający czat

    // Funkcja wysyłania wiadomości
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            const messageDiv = document.createElement('p');
            messageDiv.textContent = `Ty: ${message}`;
            chatMessages.appendChild(messageDiv);
            chatInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Obsługuje kliknięcie w przycisk "Wyślij"
    sendButton.addEventListener('click', sendMessage);

    // Obsługuje naciśnięcie klawisza Enter w polu tekstowym
    chatInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Zamknięcie czatu
    closeChatButton.addEventListener('click', function() {
        chatBox.style.display = 'none';
    });

    // Otwórz czat
    openChatButton.addEventListener('click', function() {
        chatBox.style.display = 'flex';  // Otwórz czat, ustawiając display na flex
    });
});

// Funkcja wysyłania wiadomości
function sendMessage() {
    const message = chatInput.value.trim();
    if (message) {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "send_message.php", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                chatInput.value = '';  // Czyści pole
                loadMessages();  // Ładowanie nowych wiadomości
            }
        };
        xhr.send("message=" + encodeURIComponent(message));
    }
}
// Funkcja ładowania wiadomości z PHP
function loadMessages() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "get_messages.php", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const messages = JSON.parse(xhr.responseText);
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = '';  // Czyszczenie poprzednich wiadomości
            messages.forEach(function (msg) {
                const messageDiv = document.createElement('p');
                messageDiv.textContent = msg.user + ": " + msg.message;
                chatMessages.appendChild(messageDiv);
            });
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    };
    xhr.send();
}

// Ładowanie wiadomości co 2 sekundy
setInterval(loadMessages, 2000);
