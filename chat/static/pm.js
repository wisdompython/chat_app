console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
const LoggedInUser = JSON.parse(document.getElementById('LoggedInUser').textContent)
const OtherUser= JSON.parse(document.getElementById('otherUser').textContent)
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
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/private/" + roomName + "/");

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
                const newMessage = document.createElement('div')
                newMessage.setAttribute('class','message-content')
                newMessage.setAttribute('data-author',data.sent_by)
                message_body = document.createElement("p")
                message_body.textContent = data.message
                newMessage.appendChild(message_body)
                chatLog.appendChild(newMessage)
                SortMessagesByUser()
            // if (data.sent_by==LoggedInUser){
            //     data.style.color='red'
            //     chatLog.value += data.message + "\n";
            // }
                // chatLog.value += data.message + "\n";
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
            "sent_by": LoggedInUser,
            "sent_to": OtherUser
        }));
        // console.log(JSON.parse(document.getElementById('LoggedInUser').textContent))
        chatMessageInput.value = "";
    };
}
console.log(roomName)


function SortMessagesByUser(){
    const messageContainer = document.getElementsByClassName("message-content")
    console.log(messageContainer)

    for (let i = 0, len = messageContainer.length; i < len; i++){
        console.log(messageContainer[i].getAttribute('data-author'))
        if (messageContainer[i].getAttribute('data-author')==LoggedInUser){
            // style here
            messageContainer[i].style.marginLeft="70%"
            // messageContainer[i].style.direction="rtl"
            messageContainer[i].style.float="right"
            messageContainer[i].style.display="inline-block"
            messageContainer[i].style.maxWidth="40%"
            messageContainer[i].children[0].style.overflowWrap="break-word"
            messageContainer[i].children[0].style.width="fit-content"
            messageContainer[i].children[0].style.float="right"
            messageContainer[i].children[0].style.display="inline-block"
            messageContainer[i].children[0].style.borderRadius="10px"
            messageContainer[i].children[0].style.maxWidth="100%"
            messageContainer[i].children[0].style.padding="5px"
            messageContainer[i].children[0].style.marginBottom="5px"
            messageContainer[i].children[0].style.backgroundColor="rgb(137, 100, 100)"
        }else{
           
            messageContainer[i].style.marginRight="60%"
            messageContainer[i].style.display="inline-block"
            messageContainer[i].style.maxWidth="40%"
            messageContainer[i].children[0].style.overflowWrap="break-word"
            messageContainer[i].children[0].style.overflowWrap="break-word"
            messageContainer[i].children[0].style.width="fit-content"
            messageContainer[i].children[0].style.display="inline-block"
            messageContainer[i].children[0].style.maxWidth="100%"
            messageContainer[i].children[0].style.borderRadius="10px"
            messageContainer[i].children[0].style.padding="5px"
            messageContainer[i].style.marginBottom="5px"
            messageContainer[i].children[0].style.backgroundColor="rgb(37, 150, 190)"
        }
    }
}

SortMessagesByUser();
connect();
