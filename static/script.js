function sendMessage() {
    let input = document.getElementById("userInput");
    let message = input.value.trim();

    if (message === "") return;

    let chatBox = document.getElementById("chatbox");

    // Show user message
    chatBox.innerHTML += `
        <div class="user-message">
            <div class="bubble user">${message}</div>
        </div>
    `;

    // Clear input
    input.value = "";

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send message to Flask backend
    fetch("/get", {
        method: "POST",
        body: new URLSearchParams({
            msg: message
        }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.text())
    .then(data => {
        // Create bot message with typing effect
        let botDiv = document.createElement("div");
        botDiv.className = "bot-message";

        let bubble = document.createElement("div");
        bubble.className = "bubble bot";
        bubble.innerText = "Typing...";

        botDiv.appendChild(bubble);
        chatBox.appendChild(botDiv);

        chatBox.scrollTop = chatBox.scrollHeight;

        // Replace typing with actual response
        setTimeout(() => {
            bubble.innerText = data;
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 1000);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Enter key support
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("userInput");

    if (input) {
        input.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    }
});