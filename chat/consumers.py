import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from channels.db import database_sync_to_async
from .models import *
from users.models import *
from .chatbot import *

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.bot = None

    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(room_name=self.room_name)
        room_bot = GroupRoomProfile.objects.get(room=self.room)
        if room_bot.room_bot != None:            
            self.bot = Collection.objects.get(id=room_bot.room_bot.id)
        
        # connection has to be accepted if user is authenticated and room with user in it exists
        if self.user.is_authenticated:
            room = get_object_or_404(Room, room_name=self.room_name, members__id=self.user.id)
        # connection has to be accepted
            if room:
                self.accept()


        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )


    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        sent_by = text_data_json['sent_by']
        # sent_to = text_data_json['sent_to']
        self.message = text_data_json['message']
        self.sender = CustomUser.objects.get(email=sent_by)
        print(self.message)
        
       
        if self.message.startswith("@query") and self.bot != None: 
            self.query_chatbot(self.message.replace("@query", ""), self.bot.id)
            #self.sender = CustomUser.objects.get(email=sent_by)
            
        
        else :
            Message.objects.create(
            room=self.room,
            sender=self.sender, message=self.message, group=True)
            
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.message,
                'sent_by':self.sender.email
            }
        )
            self.room.last_modified = timezone.now()
            self.room.save()
        
        #self.receiver = CustomUser.objects.get(email=sent_to)
           



    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def query_chatbot(self, query, collection):

        response = chatbot(query, collection)
        
        
        Message.objects.create(
            room=self.room,
            sender=None, message=response, group=True)
        
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': response,
            }
        )
        

class PrivateMessage(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None

    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(room_name=self.room_name)
        print(self.channel_name)

        if self.user.is_authenticated and Room.objects.filter(room_name = self.room_name, members__id=self.user.id) is not None:
        # connection has to be accepted
            self.accept()


        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        sent_by = text_data_json['sent_by']
        sent_to = text_data_json['sent_to']
        print(sent_by)
        print(sent_to)
        
        self.message = text_data_json['message']
        self.sender = CustomUser.objects.get(email=sent_by)
        self.receiver = CustomUser.objects.get(email=sent_to)
        save_message = Message.objects.create(
            room=self.room,
            sender=self.sender, 
            receiver=self.receiver, message=self.message, private=True)
        self.room.last_modified = timezone.now()
        self.room.save()
        save_message.save()

    

        
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sent_by':self.sender.email,
                'sent_to':self.receiver.email,
                'message': self.message,
            }
        )
    
    def chat(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sent_by':self.sender.email,
                'sent_to':self.receiver.email,
                'message': message,
            }
        )
    
    def send_notifications(self,event):
        print(event)
        self.send(text_data=json.dumps(
                event            
        ))
  

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))




class ChatBotConsumer(WebsocketConsumer):
    def __init__(self):
        pass

    def connect(self):
        pass

    def receive(self):
        pass


