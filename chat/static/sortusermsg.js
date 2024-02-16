const LoggedInUser = JSON.parse(document.getElementById('LoggedInUser').textContent)
const OtherUser= JSON.parse(document.getElementById('otherUser').textContent)
export function SortMessagesByUser(){
    const messageContainer = document.getElementsByClassName("message-content")
    console.log(messageContainer)
    
    for (let i = 0, len = messageContainer.length; i < len; i++){
        console.log(LoggedInUser)
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
            console.log('food')
        }else{
            console.log("good")
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
            messageContainer[i].children[0].style.backgroundColor="rgb(137, 150, 190)"
        }
    }
}