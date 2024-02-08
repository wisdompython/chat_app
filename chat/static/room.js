console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
console.log(roomName)

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");



function AddOnlineUsers(value){
    if (document.querySelector("option[value="+ value +" ]")){
        return;
    }
    let newOption = new Option(value, value)
    onlineUsersSelector.add(newOption)
}

function RemoveOnlineUser(value){
    user = document.querySelector("option[value="+ value +" ]")
    if(user!==null){
        user.remove()
    }
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    // TODO: forward the message to the WebSocket
    chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {
    console.log(roomName)
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };
    // i think when we recieve a message from the server
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "chat_message":
                chatLog.value += data.message + "\n";
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }


    // when you click on the send button this should happen

    chatMessageSend.onclick = function() {
        if (chatMessageInput.value.length === 0) return;
        chatSocket.send(JSON.stringify({
            "message": chatMessageInput.value,
        }));
        chatMessageInput.value = "";
    };
}
console.log(roomName)
connect();
