const csrftoken = getCookie('csrftoken');
export function AcceptRejectInvite(roomID){
    if(document.getElementById('AcceptInvite')){
        const InviteButton = document.getElementById('AcceptInvite')
        
        // const roomID = JSON.parse(document.getElementById('group_room_id').textContent)
        const inviteID = InviteButton.getAttribute('data-invite')
        
        InviteButton.addEventListener('click', function(e){
    
            let url = 'http://localhost:8000/chat/invite/acceptinvite/'
            // send a request with it's id to the backend
    
            fetch (url,
                {
                    method:'POST',
                    headers:{'Content-Type': 'application/json','X-CSRFToken': csrftoken},
                    body : JSON.stringify(
                        {'room_id':roomID, 'invite_id':inviteID})
                }).then((response)=>{
                    console.log(response.json())
                }).then((data)=>{
                    
                })
        })  
        
    }else if (document.getElementById('RejectInvite'))
        {
        //send a request with it's id to the bacjend
        console.log('interesting')
    } else {
        console.log('no invites')
    }
    
    
}


