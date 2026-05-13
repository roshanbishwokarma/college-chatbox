function sendMessage() {
    // Get input field and chatbox
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatbox");

    // Check if elements exist
    if (!input || !chatBox) {
        console.error("userInput or chatbox element not found.");
        return;
    }

    // Get user message
    const message = input.value.trim();

    // Stop if message is empty
    if (message === "") {
        return;
    }

    // Display user message
    chatBox.innerHTML += `
        <div class="message user">${message}</div>
    `;

    // Clear input field
    input.value = "";

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Create typing indicator
    const typing = document.createElement("div");
    typing.className = "message bot";
    typing.id = "typing";
    typing.innerHTML = "Bot is typing...";

    chatBox.appendChild(typing);
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
        // Remove typing indicator
        const typingElement = document.getElementById("typing");
        if (typingElement) {
            typingElement.remove();
        }

        // Show bot response
        chatBox.innerHTML += `
            <div class="message bot">${data}</div>
        `;

        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);

        // Remove typing indicator
        const typingElement = document.getElementById("typing");
        if (typingElement) {
            typingElement.remove();
        }

        // Show error message
        chatBox.innerHTML += `
            <div class="message bot">Error: Unable to connect to server.</div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

// Enter key support
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