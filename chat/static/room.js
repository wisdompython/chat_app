console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);

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