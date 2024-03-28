const csrftoken = getCookie('csrftoken');
var getFriends = []
friendsList = document.getElementsByClassName('check-friends')

submit_first_form = document.querySelector(".modal1").addEventListener('click', function(e){
    e.preventDefault();

    document.querySelector(".friends-selection").classList.add('hidden')
    document.querySelector(".groupProfile").classList.remove("hidden")

})
form = document.querySelector("form").addEventListener('submit', function(e){
    e.preventDefault();
    const RoomName = document.getElementById('room-title').value
    const Description = document.getElementById('Description').value

    let  url = 'http://localhost:8000/chat/group/create-group/'

            for (let i=0; i < friendsList.length; i++){

                console.log(i)
                if(friendsList[i].checked==true){
                    console.log(friendsList[i])
                    getFriends.push(Number(friendsList[i].value))

                }
                
            }
            document.querySelector("form").reset();
            console.log(getFriends)
            fetch (url, {
                method: 'POST',
                headers:{'Content-Type': 'application/json','X-CSRFToken': csrftoken},
                body : JSON.stringify({'room_name':RoomName, 'description':Description,'added_ids':getFriends})

            })
            .then((response)=>{
                return response.json()
                
            })

            .then((data)=>{
                //  here i want to send a message via websockets to all the users

                
                console.log("this is another",data)
                window.location.replace('http://localhost:8000/chat/')
            })
        })
