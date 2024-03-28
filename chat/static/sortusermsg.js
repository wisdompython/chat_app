export function SortMessagesByUser(OtherUser){
    const LoggedInUser = JSON.parse(document.getElementById('LoggedInUser').textContent)
// const OtherUser= JSON.parse(document.getElementById('OtherUser').textContent)
    const messageContainer = document.getElementsByClassName("message-content")
    for (let i = 0, len = messageContainer.length; i < len; i++){

        messageContainer[i].style.display="inline-block"
        messageContainer[i].style.maxWidth="40%"
        messageContainer[i].children[0].style.overflowWrap="break-word"
        messageContainer[i].children[0].style.width="fit-content"
        messageContainer[i].children[0].style.borderRadius="10px"
        messageContainer[i].children[0].style.maxWidth="100%"
        messageContainer[i].children[0].style.padding="5px"
        messageContainer[i].children[0].style.marginBottom="5px"
        if (messageContainer[i].getAttribute('data-author')==LoggedInUser){
            // style here
            messageContainer[i].style.marginLeft="70%"
            // messageContainer[i].style.direction="rtl"
            messageContainer[i].style.float="right"
            messageContainer[i].children[0].style.float="right"
            messageContainer[i].children[0].style.backgroundColor="rgb(137, 100, 100)"
        }else{
            messageContainer[i].style.marginRight="60%"
            messageContainer[i].children[0].style.backgroundColor="rgb(137, 150, 190)"
        }
    }
}

export function HandleGroupInvitesNotification(message){
    const notification = document.createElement('div')
    notification.setAttribute('class','message-content')
    notification.setAttribute('data-author',data.sent_by)
    const notification_wrapper = document.createElement('div')
    notification_wrapper.setAttribute('class','group-invite')
    const notification_text = document.createElement("p")
    notification_text.setAttribute('class','invite-message')
    notification_text.textContent = message
    const accept_btn = document.createElement('button')
    const reject_btn = document.createElement('button')
    accept_btn.textContent = 'Accept Invite'
    reject_btn.textContent = 'Reject Invite'
    accept_btn.setAttribute('id','AcceptInvite')
    accept_btn.setAttribute('class','accept-invite')
    reject_btn.setAttribute('id','RejectInvite')
    reject_btn.setAttribute('class','reject-invite')
    accept_btn.setAttribute('data-invite', data.invite_id)
    reject_btn.setAttribute('data-invite', data.invite_id)
    notification_wrapper.appendChild(notification_text)
    notification_wrapper.appendChild(accept_btn)
    notification_wrapper.appendChild(reject_btn)
    notification.appendChild(notification_wrapper)
    chatLog.appendChild(notification)
}