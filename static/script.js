function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();

    if (message === "") return;

    let chatBox = document.getElementById("chat-box");

    // User message
    chatBox.innerHTML += `
        <div class="user-message">
            <div class="bubble user">${message}</div>
        </div>
    `;

    fetch("/get", {
        method: "POST",
        body: new URLSearchParams({ msg: message }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.text())
    .then(data => {
    // Create bot message container
    let botDiv = document.createElement("div");
    botDiv.className = "bot-message";

    let bubble = document.createElement("div");
    bubble.className = "bubble bot";
    bubble.innerText = "Typing...";

    botDiv.appendChild(bubble);
    chatBox.appendChild(botDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    // Replace typing with actual message
    setTimeout(() => {
        bubble.innerText = data;
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 1000);
});
    input.value = "";
}

// Enter key support
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});