from django.db import models
from users.models import *
import uuid
import os
# Create your models here.

def get_upload_path(instance, filename):
      print(instance)
      return os.path.join('collections', instance.document_folder_name, filename)
class Collection(models.Model):
    #api_key = models.ForeignKey(APIKey, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class DataSource(models.Model):
    document_folder_name = models.CharField(max_length=1000)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path, max_length=1000)   

class LearningAssistantChatRoom(models.Model):
    room_name = models.CharField(max_length=500)
    bot = models.ForeignKey(Collection, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class BotConversations(models.Model):
    name = models.CharField(max_length=200)
    room = models.ForeignKey(LearningAssistantChatRoom,on_delete=models.CASCADE)

class UserQueries(models.Model):
    conversation = models.ForeignKey(BotConversations,on_delete=models.CASCADE)
    message = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class BotUserMessage(models.Model):
    conversation = models.ForeignKey(BotConversations,on_delete=models.CASCADE)
    message = models.TextField()
    creator = models.ForeignKey(Collection, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(UserQueries, on_delete=models.CASCADE, null=True)


class Message(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, null=True, related_name='room_messages')
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE, null=True, blank=True, default=None)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', default=None, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    private = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    timestamp =models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    room_name = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True) 
    room_title = models.CharField(null=True, blank=True, max_length=200)  
    members = models.ManyToManyField(CustomUser, blank=True)
    private = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    timestamp =models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    
    
    def get_online_count(self):
        return self.members.count()

    def join(self,user):
        self.online.add(user)
    
    def leave(self,user):
        self.online.remove(user)
    
    def __str__(self):
        return f'{self.room_name} : {self.get_online_count()}'
    
    class Meta:
        ordering = ['timestamp']
    

class GroupRoomProfile(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="group_room")
    room_title_caption= models.CharField(max_length=100, null=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room_bot = models.ForeignKey(Collection, default=None, blank=True, null=True, on_delete=models.CASCADE)
    room_description = models.TextField(null=True)



class GroupInvite(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='group_room_invite')
    sender = models.ForeignKey(CustomUser, related_name='group_invite_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='group_invite_receiver', on_delete=models.CASCADE)
    pending = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    timestamp =models.DateTimeField(auto_now_add=True)


