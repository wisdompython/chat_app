from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=100)
    online = models.ManyToManyField(User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self,user):
        self.online.add(user)
    
    def leave(self,user):
        self.online.remove(user)
    
    def __str__(self):
        return f'{self.room_name} : {self.get_online_count()}'
    
    

class Message(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp =models.DateTimeField(auto_now_add=True)
