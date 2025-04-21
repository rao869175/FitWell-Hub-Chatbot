document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("chatForm").addEventListener("submit", function(e) {
        e.preventDefault();

        const userInput = document.getElementById("userInput").value;

        fetch("/get-response", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            const responseArea = document.getElementById("responseArea");
            const responseDiv = document.createElement("div");
            responseDiv.classList.add("chat-bubble");
            responseDiv.textContent = data.response;
            responseArea.appendChild(responseDiv);
            document.getElementById("chatForm").reset();
        })
        .catch(error => console.error("Error:", error));
    });
});
