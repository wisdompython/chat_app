function connect(roomName) {
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
                let message_body = document.createElement("p")
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


    chatSocket.send = function(e){
        
    }
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