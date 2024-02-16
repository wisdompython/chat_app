from django.shortcuts import render, redirect,get_object_or_404

# Create your views here.
from chat.models import *
from users.models import *
from .forms import *
from .chatbot import *
import uuid

def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.filter(online__id=request.user.id),
    })

def private_chat(request):
    # view all the rooms a user is present in
    group_chats = Room.objects.filter(members__id=request.user.id)
    private_room = PrivateRooms.objects.filter(users__id=request.user.id)
    #print(private_room)
    print(group_chats)
    return render(request,'user_view.html', {
        'users':private_room,
        'groups':group_chats
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



def chat_bot_room(request, bot_name):
    pass

def add_datasource(request):
    print(request.user.id)
    form = CreateDataSource(current_user=request.user)
    if request.method=='POST':
        form = CreateDataSource(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)

            instance.owner = request.user
            instance.save()

        else:
            print(form.errors)
            form = CreateDataSource(current_user=request.user)

    return render(request, 'add_datasource.html', {'form':form})
def add_collection(request):
    form = CreateCollection()

    if request.method=='POST':
        form = CreateCollection(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
        else:
            form = CreateCollection()

    return render(request, 'add_datasource.html', {
        'form':form
    })

def view_all_collections(request):
    collections = Collection.objects.filter(owner=request.user)

    return render(request, 'view_collection.html', {
        'collections':collections
    })


#query both and return response, will likely tie this with ajax so i can stream the response
def query_collection(request, collection_id):
    form = QueryBot()
    if request.method=='POST':
        form = QueryBot(request.POST)
        if form.is_valid():
            model = chatbot(form.cleaned_data['query'], collection_id)
            print(model)  
    return render(request, 'query.html', {
        'form':form
    })

# we want to enter into a room
def room_view(request, room_name):
    chat_room = get_object_or_404(Room, room_name=room_name)
    # check if the user is a member of that room
    if chat_room:
        print(chat_room.online.all())
        if not request.user in chat_room.members.all():
            return redirect('home')
        

    return render(request, 'chat_room.html', {
        'room': chat_room,
    }) 
def CreateGroupChat(request):
    form = CreateGroupChatForm(current_user=request.user.id)

    if request.method=='POST':
        form = CreateGroupChatForm(request.POST, current_user=request.user.id)

        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user.id 
    pass
def InviteToGroupChat(request, groupID, user_id):
    room = Room.objects.get(id=groupID)
    invite = GroupInvite.objects.create(room=room, sender=request.user, receiver=user_id)
     ## create a notification
    pass

def AcceptGroupInvite(request, groupID, inviteID):
    room = Room.objects.get(id=groupID)

    

    pass