function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatbox");

    if (!input || !chatBox) {
        console.error("Input box or chatbox not found.");
        return;
    }

    const message = input.value.trim();

    if (message === "") {
        return;
    }

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

    // Show typing indicator
    const botDiv = document.createElement("div");
    botDiv.className = "bot-message";

    const bubble = document.createElement("div");
    bubble.className = "bubble bot";
    bubble.innerText = "Typing...";

    botDiv.appendChild(bubble);
    chatBox.appendChild(botDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    // Send message to Flask backend
    fetch("/get", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "msg=" + encodeURIComponent(message)
    })
    .then(response => response.text())
    .then(data => {
        bubble.innerText = data;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        bubble.innerText = "Error: Unable to connect to server.";
        console.error("Fetch error:", error);
    });
}

// Run after page loads
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("userInput");

    if (input) {
        input.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });
    }
});