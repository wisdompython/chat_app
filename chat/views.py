from django.shortcuts import render, redirect

# Create your views here.
from chat.models import *
from users.models import *
import uuid

def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })

def private_chat(request):
    # view all the rooms a user is present in
    private_room = PrivateRooms.objects.filter(users__id=request.user.id)
    
    return render(request,'user_view.html', {
        'users':private_room
    })

# enter a particular room
def private_chat_rooms(request,user_id):
    user_exists = CustomUser.objects.filter(id=user_id).exists()
    if not user_exists:
        return redirect('home')
    get_user_messages = PrivateMessage.objects.filter(sender=request.user, 
                                    receiver=user_id)|PrivateMessage.objects.filter(sender=user_id,
                                                                                    receiver=request.user) 
    private_room = PrivateRooms.objects.filter(users__in=[request.user.id, user_id]).exists()
    if not private_room:  
        if user_exists:
            private_room = PrivateRooms.objects.create()
            private_room.users.add(request.user)
            private_room.users.add(user_id)
    logged_in_user = CustomUser.objects.get(id=request.user.id)
    other_user = CustomUser.objects.get(id=user_id)
    private_room = PrivateRooms.objects.filter(users__in=[request.user.id, user_id])
    return render(request,'private_messaging.html',
                    {'private_room':private_room[0], 'messages':get_user_messages,
                     'logged_in_user':logged_in_user,'other_user':other_user})

def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(room_name=room_name)
    return render(request, 'chat_room.html', {
        'room': chat_room,
    })

def chat_bot_room(request, bot_name):
    pass