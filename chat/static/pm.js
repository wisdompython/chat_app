import {SortMessagesByUser} from './sortusermsg.js';
import { HandleGroupInvitesNotification } from './sortusermsg.js';

let chatSocket = null
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");

export function connect(roomName, OtherUser, url_tag) {
    let chatLog = document.querySelector(".chat-box-container");
    let message_area = document.querySelector('.chat-with-user')

    chatMessageInput.focus();
    const LoggedInUser = JSON.parse(document.getElementById('LoggedInUser').textContent)
    chatMessageInput.onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter key
            chatMessageSend.click();
        }
    };

    chatMessageSend.onclick = function() {
        if (chatMessageInput.value.length === 0) return;
        chatMessageInput.value = "";
    };
    chatLog.scrollTop = chatLog.scrollHeight

    if(chatSocket && chatSocket.readyState === WebSocket.OPEN){
        chatSocket.close()
    }

    chatSocket = new WebSocket("ws://" + window.location.host + url_tag + roomName + "/");
    
    
    console.log(chatSocket.readyState)
    chatSocket.onopen = function(e) {
        console.log(chatSocket.readyState)
      
        console.log("Successfully connected to the WebSocket.");
    }
    

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        
    
        switch (data.type) {
            case "chat_message":
                const newMessage = document.createElement('div')
                newMessage.setAttribute('class','message-content')
                newMessage.setAttribute('data-author',data.sent_by)
                newMessage.innerHTML = `<p> ${(data.message)} </p>`
                message_area.appendChild(newMessage)
                chatLog.scrollTop = chatLog.scrollHeight
                SortMessagesByUser(OtherUser)
                break;
            case "send_notifications":
                HandleGroupInvitesNotification(data.message)
                SortMessagesByUser(OtherUser)
                console.log(data)
                break;
        }
        
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }


    chatMessageSend.onclick = function() {
        if (chatMessageInput.value.length === 0) return;
        chatSocket.send(JSON.stringify({
            "message": chatMessageInput.value,
            "sent_by": LoggedInUser,
            "sent_to": OtherUser,
            "type":"chat_message"
        }));
        chatMessageInput.value = "";
    };
    return chatSocket
}

