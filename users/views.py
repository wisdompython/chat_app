from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.core import serializers
# Create your views here.
from .models import *
from chat.models import *

def check_if_firends(logged_in_user, other_user_id):
    if logged_in_user.id == other_user_id:
        return None
    return UserFriends.objects.filter(user=logged_in_user.id, friends=other_user_id).exists()
def ViewUserProfile(request, user_id):

    profile = UserProfile.objects.get(user=user_id)

    return render(request, 'users/view_profile.html', {
        'profile_data' :profile,
        'is_friends':check_if_firends(request.user, user_id)
    })

def EditUserProfile(request,user_id):
    pass
def FindFriends(request):

    if request.method == 'GET':
        search_query = request.GET.get('user-search')
        print(search_query)
        results = CustomUser.objects.filter(email__contains=search_query)
        print(results)
        return render(request, 'user_search.html', {
            'results':results
        })
    else:
        return render(request, 'user_search.html')
    
def testsearch(request, user_mail):
    if request.method == 'GET':
        users = CustomUser.objects.filter(email__contains=user_mail)
        search_results = serializers.serialize('json',CustomUser.objects.filter(email__contains=user_mail), fields=["email","firstname"])
        room = serializers.serialize('json',Room.objects.filter(members__in=users))
        print(room)
        print(search_results)
        return JsonResponse({
            'data':search_results, 'room':room
        })
    

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
