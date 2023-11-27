room_input = document.querySelector("#roomInput")
document.querySelector("#roomInput").focus()

// redirect to a room
document.querySelector("#roomConnect").onclick = function(){
    let roomname = document.querySelector("#roomInput").value; 
    window.location.pathname = "chat/" + roomname +"/";
}

// if user submits with the enter key
document.querySelector("#roomConnect").onkeyup = function(e){
    if (e.keyCode == 13){
        document.querySelector("#roomConnect").click()
    }
}

document.querySelector("#roomSelect").onchange = function() {
    let roomname = document.querySelector("#roomSelect").value.split(" (")[0];
    window.location.pathname = "chat/" + roomname +"/";
}