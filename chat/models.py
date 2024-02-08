from django.db import models
from users.models import CustomUser

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
    
    

class Message(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    message = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp =models.DateTimeField(auto_now_add=True)

# i am trying to achieve 
class PrivateMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.message}"

class OneOnOneMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='oneonone_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='oneonone_received_messages', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.message}"
