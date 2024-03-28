import {SortMessagesByUser} from './sortusermsg.js';
import { HandleGroupInvitesNotification } from './sortusermsg.js';
import { AcceptRejectInvite } from './pm_invites.js';
import { connect } from './pm.js';
const Room = document.getElementsByClassName('chat-item')
const LoggedInUser = JSON.parse(document.getElementById('LoggedInUser').textContent)
const LoggedInUserID = JSON.parse(document.getElementById('LoggedInUserID').textContent)
console.log(LoggedInUserID)
// const OtherUser= JSON.parse(document.getElementById('OtherUser').textContent)
let current_no = 20
let message_area = document.querySelector('.chat-with-user')
let message_box_cont = document.querySelector('.chat-box-container')

console.log(Room)
export function GetData (url){
        let data = fetch (url, {
            method: 'GET',
            headers:{'Content-Type': 'application/json'},
        }).then((response)=>{
            let value =  response.json()
            console.log(value)
            return value
        })
        return data
    }

function RenderChatMessages(chat_messages){
    document.querySelector('.chat-box-container').classList.remove('hidden')
    for (let i=0, message=chat_messages.length; i < message ; i++ ){
        
        let message_box = document.createElement('div')
        message_box.setAttribute('class','message-content')
        message_box.setAttribute('data-author',chat_messages[i].sender)
        if(chat_messages[i].message){
            message_box.innerHTML = `<p> ${chat_messages[i].message} </p>`
            
        }else if (chat_messages[i].pending){
            if (chat_messages[i].receiver == LoggedInUser )
            {
                message_box.innerHTML = `
                <div class="group-invite">
                    <p class="invite-message"></p>${chat_messages[i].sender}is inviting you to join ${chat_messages[i].group_caption.room_title_caption}
                    <button id="AcceptInvite" class="accept-invite" href="" data-invite="${chat_messages[i].id}">Accept</button>
                    <button id="RejectInvite" class="reject-invite" href="" data-invite="${chat_messages[i].id}">Reject</button>
                </div>
                <p> ${chat_messages[i].sender} is inviting you to join ${chat_messages[i].group_caption.room_id} </p>
                `
                AcceptRejectInvite(chat_messages[i].group_caption.room_id)
             }
             else {
                message_box.innerHTML = `<p> You sent an invite</p>`
                console.log('nothing')
             }
           
          
        }
        message_area.appendChild(message_box)
        SortMessagesByUser(OtherUser)
        // message_area.scrollTop = message_area.scrollHeight
        var element = document.querySelector(".chat-box-container");
        
        element.scrollTop = element.scrollHeight;
    
    }
}

// function RenderGroupMessages(chat_messages){


// }

export function SelectMessage(current_room){
    console.log(current_room)
    current_room.addEventListener('click', function(){
        document.querySelector('.default-display').classList.add('hidden')
        document.querySelector('.input-group').classList.remove('hidden')
        var OtherUser = current_room.getAttribute('data-email')
        if (message_area.childNodes){
           
            message_area.innerHTML =''
        }
        if (current_room.getAttribute('data-group')){
            
            connect(current_room.getAttribute('data-room'), OtherUser, '/ws/chat/')

            let  url =  `/chat/groups/${current_room.getAttribute('data-room')}/${current_no}/` 
            // i need to call the functions for group chat here
            
            let data  = GetData(url).then((data)=>{
                let chat_messages = data
                console.log(chat_messages)
                if(chat_messages.data){
                    RenderChatMessages(chat_messages.data)
                }
                
                // if(!chat_messages){
                //     console.log('no messages in this group')
                // }
                // 
            
            })
        }else {
            
            connect(current_room.getAttribute('data-room'), OtherUser, '/ws/chat/private/')
    
            if (message_area.childNodes){
           
                message_area.innerHTML =''
            }
            let url = `/chat/message/${Number(current_room.getAttribute('data-id'))}/${current_no}/`
    
            let data  = GetData(url).then((data)=>{
                let chat_messages = data
                if(chat_messages.data){
                    RenderChatMessages(chat_messages.data)
                }
            
            })
    
    }

        

        // make a request to get data about the roo

    })

}
for(let room_no = 0, room = Room.length; room_no < room; room_no++){
    let current_room = Room[room_no]

    SelectMessage(current_room)
   
}