const socket = io('wss://library-website-1kdk.onrender.com/');

document.getElementById("chat-button").addEventListener("click", function () {
    // let username = document.getElementById("username").value;

    socket.connect();

    socket.on("connect", function () {
        console.log("before")
        socket.emit("user_join", "library_guest");
        console.log("in connect operations")
    })
    if (document.getElementById("chat").style.display == "none"){
    document.getElementById("chat").style.display = "block";
    }
    else {
        document.getElementById("chat").style.display = "none";
    }
})

document.getElementById("message").addEventListener("keyup", function (event) {
    console.log("before message")
    let message = document.getElementById("message").value;
    if (event.key == "Enter" && message) {
        console.log('in event.key')
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