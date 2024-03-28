import { GetData, SelectMessage } from "../index.js";
const debounce = (callback, wait) => {
	let timeoutId = null;
	return (...args) => {
	  window.clearTimeout(timeoutId);
	  timeoutId = window.setTimeout(() => {
		callback.apply(null, args);
	  }, wait);
	};
  }
const LoggedInUser = JSON.parse(document.getElementById('LoggedInUser').textContent)
const LoggedInUserID = JSON.parse(document.getElementById('LoggedInUserID').textContent)
var search_input = document.querySelector('.search-for-users')
search_input.addEventListener('keyup', debounce(function(){
	let result_box = document.querySelector('.search-drop-box')
	result_box.innerHTML = ''
    // send a request 
    let url = `http://localhost:8000/users/test_search/${search_input.value}`

	let results = GetData(url).then((data)=>{
		let value = JSON.parse(data.data)
		let room  = JSON.parse(data.room)
		console.log(room[0]['fields']['members'].includes(LoggedInUserID))
		for(let i=0, len = value.length; i < len; i++){	
			// check if logged in user and the user searched for are present in the room and is private
			
			let result_item = document.createElement('div')
			result_item.setAttribute('class','result')
			let result_text = document.createElement('p')
			result_text.textContent = value[i]['fields']['email']
			result_item.appendChild(result_text)
			result_box.appendChild(result_item)	
		}
		result_box.classList.remove('hidden')
		let search_results = document.getElementsByClassName('result')
		for (let k = 0, item = search_results.length; k < item , k++;){

			search_results[k].addEventListener('click',function(){
				
				
			if (room[i]['fields']['members'].includes(value[i]['pk']) && 
			room[i]['fields']['members'].includes(LoggedInUserID) && room[i]['fields']['private']==true)
			{	
				console.log(document.querySelector('.result'))
				for (let k = 0, item = result_item.length; k < item; k++){
				console.log(item)
}
				search_results[k].setAttribute('class', 'chat-item')
				search_results[k].setAttribute('data-room', room[i]['pk'])
				search_results[k].setAttribute('data-id', value[i]['pk'])
				search_results[k].setAttribute('data-email', value[i]['fields']['email'])
				
				SelectMessage(search_results[k])
			}else {
				search_results[k].addEventListener('click', function(){
					window.location.href = `http://localhost:8000/users/user_profile/${value[i]['pk']}`
				})
			}
			})

		}
		
		})
		
	})
    	
, 2500)

// for (let k = 0, item = result_item.length; k < item; k++){
// 	console.log(item)
// }