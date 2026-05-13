function sendMessage() {
    let input = document.getElementById("userInput");
    let message = input.value.trim();

    if (message === "") return;

    let chatBox = document.getElementById("chatbox");

    // USER MESSAGE
    chatBox.innerHTML += `
        <div class="message user">${message}</div>
    `;

    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    // Typing indicator
    let typing = document.createElement("div");
    typing.className = "message bot";
    typing.id = "typing";
    typing.innerHTML = "Bot is typing...";

    chatBox.appendChild(typing);

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

        let typingElement = document.getElementById("typing");

        if (typingElement) {
            typingElement.remove();
        }

        chatBox.innerHTML += `
            <div class="message bot">${data}</div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.log(error);
    });
}

// ENTER KEY SUPPORT
document.addEventListener("DOMContentLoaded", function() {

    let input = document.getElementById("userInput");

    if (input) {
        input.addEventListener("keypress", function(event) {

            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }

        });
    }

});