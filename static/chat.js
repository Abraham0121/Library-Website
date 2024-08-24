const socket = io({ autoConnect: false });

document.getElementById("chat-button").addEventListener("click", function () {
    // let username = document.getElementById("username").value;

    socket.connect();

    socket.on("connect", function () {
        socket.emit("user_join", "library_guest");
    })
    if (document.getElementById("chat").style.display == "none"){
    document.getElementById("chat").style.display = "block";
    }
    else {
        document.getElementById("chat").style.display = "none";
    }
})

document.getElementById("message").addEventListener("keyup", function (event) {
    let message = document.getElementById("message").value;
    if (event.key == "Enter" && message) {
        socket.emit("new_message", message);
        document.getElementById("message").value = "";
    }
})

socket.on("chat", function (data) {
    let ul = document.getElementById("chat-messages");
    let li = document.createElement("li");
    li.appendChild(document.createTextNode(data["username"] + ": " + data["message"]));
    ul.appendChild(li);
    ul.scrolltop = ul.scrollHeight;
})