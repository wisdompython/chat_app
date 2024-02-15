from django.db import models
from users.models import CustomUser
import uuid
import os
# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=100)
    online = models.ManyToManyField(CustomUser, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self,user):
        self.online.add(user)
    
    def leave(self,user):
        self.online.remove(user)
    
    def __str__(self):
        return f'{self.room_name} : {self.get_online_count()}'
    

class PrivateRooms(models.Model):
    room_name = models.UUIDField(default=uuid.uuid4(),editable=True,unique=True)
    users = models.ManyToManyField(CustomUser, blank=True)

class Message(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    message = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp =models.DateTimeField(auto_now_add=True)

# i am trying to achieve 
    
class PrivateMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.message}"

class OneOnOneMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='oneonone_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='oneonone_received_messages', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.message}"

def get_upload_path(instance, filename):
      return os.path.join('collections', instance.title, filename)


class DataSource(models.Model):
    document_name = models.CharField(max_length=200)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')


class Collection(models.Model):
    #api_key = models.ForeignKey(APIKey, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    model = models.FileField(upload_to=get_upload_path)
    processing = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.title

# class LearningAssistantChatRoom(models.Model):
#     room_name = models.CharField()
#     bot = models.ForeignKey(Collection)
#     user = models.ForeignKey(CustomUser)

# class BotConversations(models.Model):
#     name = models.CharField(max_length=200)
#     room = models.ForeignKey(LearningAssistantChatRoom,on_delete=models.CASCADE)

# class BotUserMessage(models.Model):
#     conversation = models.ForeignKey(BotConversations,on_delete=models.CASCADE)
#     message = models.TextField()
#     creator = models.ForeignKey(Collection, on_delete=models.CASCADE)

# class UserQueries(models.Model):
#     conversation = models.ForeignKey(BotConversations,on_delete=models.CASCADE)
#     message = models.TextField()
#     creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
