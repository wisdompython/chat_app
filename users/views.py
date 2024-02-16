from django.shortcuts import render
from django.db import transaction
# Create your views here.
from .models import *
from chat.models import *
def ViewUserProfile(request):
    pass

def SendFriendRequest(request, user_id):
    user = request.user
    friend_request, created = FriendRequest.objects.get_or_create(sender=user, receiver=user_id)
    # one the front end this will be a button and will also trigger a notification send
    pass
@transaction.atomic # ensures that either the entire process happens or it fails, i should do this for some other models
def AcceptFriendRequest(request, friendRequestID):
    friend_request = FriendRequest.objects.get(id=friendRequestID)

    if request.user == friend_request.receiver:
        add_friend_receiving = UserFriends.objects.create(user=request.user, friends=friend_request.sender)
        add_friend_sender = UserFriends.objects.create(user=friend_request.sender, friends=request.user)

        friend_request.accepted = True
        friend_request.pending = False
        friend_request.rejected = False

        friend_request.save()
    

def RejectFriendRequest(request, FriendRequestID):

    friend_request =  FriendRequest.objects.get(id=FriendRequestID)

    friend_request.rejected = True
    friend_request.accepted = False
    friend_request.pending = False
    pass

def ViewFriends(request):
    friends = UserFriends.objects.filter(user=request.user)
    pass


def ViewNotifications(request):
    pass
