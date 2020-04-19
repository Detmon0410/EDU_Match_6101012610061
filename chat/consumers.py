# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from match.models import ChatLog


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # when user join chat room will sent contact to websocket
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        if not ChatLog.objects.filter(chatroom=self.room_name).exists():
            chat = ChatLog.objects.create(chatroom=self.room_name)
            chat.save()
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group dis contact from websocket
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        Chat = ChatLog.objects.get(chatroom=self.room_name)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        # Receive and sending message from room group
        message = event['message']
        chat = ChatLog.objects.get(chatroom=self.room_name)
        chat.chat_log += message + '\n'
        chat.save()
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
