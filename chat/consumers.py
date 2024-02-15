import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, PrivateMessage as PM
from users.models import *

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(room_name=self.room_name)

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
        message = text_data_json['message']

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )


    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

class PrivateMessage(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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
        sent_by = text_data_json['sent_by']
        sent_to = text_data_json['sent_to']
        message = text_data_json['message']
        sender = CustomUser.objects.get(email=sent_by)
        receiver = CustomUser.objects.get(email=sent_to)
        save_message = PM.objects.create(sender=sender, receiver=receiver, message=message)
        save_message.save()

        print(self.scope)
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sent_by':sender.email,
                'sent_to':receiver.email,
                'message': message,
            }
        )
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))


class ChatBotConsumer(WebsocketConsumer):
    def __init__(self):
        pass

    def connect(self):
        pass

    def receive(self):
        pass