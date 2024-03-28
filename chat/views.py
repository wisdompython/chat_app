from django.shortcuts import render, redirect,get_object_or_404
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.models import *
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.utils import timezone
from users.models import *
from .forms import *
from .chatbot import *
import uuid
import json
from itertools import chain
from operator import attrgetter

def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.filter(members__id=request.user.id).order_by('-last_modified'),
    })

def private_chat(request):
    # view all the rooms a user is present in
    rooms = Room.objects.filter(members__id=request.user.id)
    return render(request,'user_view.html', {
        'rooms':rooms
    })

def set_model_items_to_list(data):
    item_list = []
    for item in data:
        print(item.receiver)
        try:
            if item.message and item.receiver:
                item_info = {
                    'sender':item.sender.email,
                    'receiver':item.receiver.email,
                    'message': item.message,
                    'timestamp':item.timestamp,
                    'room_name': item.room.room_name,
                }
            elif item.message and item.sender :
                item_info = {
                    'sender':item.sender.email,
                    'message': item.message,
                    'timestamp':item.timestamp,
                    'room_name': item.room.room_name,
                }
            else:
                item_info = {
                    'message': item.message,
                    'timestamp':item.timestamp,
                    'room_name': item.room.room_name,
                }

        except Exception as e:
            print(e)
            try:
                if item.pending:
                    item_info = {
                        'sender':item.sender.email,
                        'receiver':item.receiver.email,
                        'pending': item.pending,
                        'room_name': item.room.room_name,
                        'group_caption' : item.room.group_room.values()[0],
                        'timestamp':item.timestamp
                    }
                    print(item_info)
            except Exception as e:
                print(e)
                return {"error":"no item"}


        item_list.append(item_info)

    return item_list

# enter a particular room
def private_chat_rooms(request,user_id, num):
    user_exists = CustomUser.objects.filter(id=user_id).exists()
    if not user_exists:
        return redirect('home')
    elif not UserFriends.objects.filter(user=request.user.id, friends=user_id).exists():
        return redirect('home') # i want to tell them this person is not on your friend list 
    
    get_user_messages = Message.objects.filter( Q(sender=request.user.id, 
                                    receiver=user_id, private=True)| Q (sender=user_id,
                                                                                    receiver=request.user.id, private=True))
    
    get_invites = GroupInvite.objects.filter(
        Q(sender=request.user.id, receiver=user_id, pending=True) | Q(
        sender=user_id, receiver=request.user.id, pending=True))
    combined_query_set = list(chain(sorted(get_user_messages,key=attrgetter('timestamp')), sorted(get_invites,key=attrgetter('timestamp'))))
    combined_query_set = sorted(combined_query_set, key=attrgetter('timestamp'))
    message = set_model_items_to_list(combined_query_set[-num:])
    private_room = Room.objects.filter(members=request.user.id, private=True).filter(members=user_id).exists()
    if not private_room:  
        if user_exists:
            private_room = Room.objects.create()
            private_room.members.add(request.user)
            private_room.members.add(user_id)
            private_room.private=True
            private_room.save()
    logged_in_user = CustomUser.objects.get(id=request.user.id)
    other_user = CustomUser.objects.get(id=user_id)
    print(other_user)

    private_room = Room.objects.filter(members=logged_in_user, private=True).filter(members=user_id)

    return JsonResponse({
        'data':message,
        'logged_in_user':logged_in_user.email,
        'other_user':other_user.email
    })
   

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
def SendInvites(userIDs:list):
    for user_id in userIDs:
        pass

def getUser(user_id):
    return CustomUser.objects.get(id=user_id)

def check_if_friends_room(loggedIn, otherUser):
    return Room.objects.filter(members=otherUser, private=True).filter(members=loggedIn).exists()

def GroupChat(request, room_name, num):
    print(room_name)
    # check if room exists
    get_group = Room.objects.filter(room_name=room_name,group=True, members__id=request.user.id ).exists()
    if get_group:
        # if yes get room

        get_group = Room.objects.get(room_name=room_name)
        ## check if user is a member of the room
        
        
        get_room_messages = Message.objects.filter(room=get_group, group=True)

        get_room_messages = set_model_items_to_list(list(get_room_messages)[-num:])
        print(get_room_messages)

        return JsonResponse({
            'data':get_room_messages,
            'logged_in_user': request.user.email
            })
    
    return JsonResponse("not a member of this group", safe=False)

def CreateGroupChat(request):
    get_user_friends = UserFriends.objects.filter(user=request.user.id)
    if request.method=='POST':
            form = json.loads(request.body)
            print(form)
            friends = form['added_ids']

            group_room = Room.objects.create(group=True)
            group_room.members.add(request.user)
            group_profile = GroupRoomProfile.objects.create(room=group_room, 
                                             room_title_caption=form['room_name'],
                                             room_description = form['description'],
                                             creator = request.user)
            group_profile.save()
            for friend in range(len(friends)):
                get_user = getUser(friends[friend])
                room = check_if_friends_room(get_user, request.user)
                if not room:
                    Room.objects.create(private=True).members.add(request.user, get_user)
                room = Room.objects.filter(members=get_user, private=True).filter(members=request.user)
                invite = GroupInvite.objects.filter(room=group_room, sender=request.user.id).filter(receiver=get_user).exists()
                if not invite:
                    invite = GroupInvite.objects.create(room=group_room, sender=request.user, receiver=get_user)
                invite = GroupInvite.objects.get(room=group_room, sender=request.user, receiver=get_user)
                channel_layer = get_channel_layer()

                async_to_sync(channel_layer.group_send)(
                    f'chat_{room[0].room_name}',
                    {
                        'message': json.dumps(f"{request.user} is inviting you to join his group"),
                        'invite_id':invite.id,
                        'sent_by':json.dumps(request.user.email),
                        'sent_to':get_user.email,
                        'type':'send_notifications'
                    })
            return JsonResponse({'data':'Group Created'},status=200)
    return render (request, 'create_group_chat.html',{"friends":get_user_friends})

def InviteToGroupChat(request, groupID, user_id):
    check_if_owner_of_group  = get_object_or_404(Room, creator=request.user.id)
    room = Room.objects.get(id=groupID)
    check_if_friends = get_object_or_404(UserFriends, user=request.user, friends=user_id)

    if check_if_friends: 
        check_if_member_of_group = get_object_or_404(Room, members__id=user_id)
    invite = GroupInvite.objects.create(room=room, sender=request.user, receiver=user_id)
     ## create a notification
    pass


@transaction.atomic
def AcceptGroupInvite(request):
    if request.method=='POST':
        data = json.loads(request.body)
        print(data)
        print(data['room_id'])
        room = Room.objects.get(room_name=data['room_id'])
        print(room)
        invite = GroupInvite.objects.filter(room=room, receiver=request.user).exists()
        if invite:
            invite = GroupInvite.objects.get(room=room, receiver=request.user)
            room.members.add(request.user.id)
            invite.accepted=True    
            invite.rejected= False
            invite.pending=False
            invite.save()
            room.save()
            return JsonResponse("Completed!!", safe=False)
    return JsonResponse("Failed", safe=False)


@transaction.atomic
def RejectGroupInvite(request):
    if request.method=='POST':
        data = json.loads(request.body)
        print(data)
        print(data['room_id'])
        room = Room.objects.get(room_name=data['room_id'])
        print(room)
        invite = GroupInvite.objects.filter(room=room, receiver=request.user).exists()
        if invite:
            invite = GroupInvite.objects.get(room=room, receiver=request.user)
            invite.accepted=False   
            invite.rejected= True
            invite.pending=False
            invite.save()
            room.save()
            return JsonResponse("Completed!!", safe=False)
    return JsonResponse("Failed", safe=False)
