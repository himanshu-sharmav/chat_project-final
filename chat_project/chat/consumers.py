import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Room, Message
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope['user']
            self.other_username = self.scope['url_route']['kwargs']['room_name']
            
            # Add user to online users
            await self.add_online_user()
            
            # Get or create room
            self.room = await self.get_or_create_room()
            self.room_group_name = str(self.room.name)

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            
            # Broadcast online users update
            await self.broadcast_online_users()
            
            # Send existing messages
            messages = await self.get_messages()
            for message in messages:
                await self.send(text_data=json.dumps(message))
                
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            raise

    @database_sync_to_async
    def get_or_create_room(self):
        User = get_user_model()
        other_user = User.objects.get(username=self.other_username)
        return Room.get_or_create_room(self.user, other_user)

    @database_sync_to_async
    def get_messages(self):
        messages = Message.objects.filter(room=self.room).select_related('sender')
        return [{
            'content': msg.content,
            'sender': msg.sender.username,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]

    @database_sync_to_async
    def save_message(self, content):
        User = get_user_model()
        try:
            receiver = User.objects.get(username=self.other_username)
            return Message.objects.create(
                room=self.room,
                sender=self.user,
                receiver=receiver,
                content=content
            )
        except User.DoesNotExist:
            return None

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Save message
        msg = await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': msg.timestamp.isoformat() if msg else None
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event.get('timestamp')
        }))

    async def disconnect(self, close_code):
        try:
            # Remove user from online users
            await self.remove_online_user()
            
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            
            # Broadcast online users update
            await self.broadcast_online_users()
            
        except Exception as e:
            logger.error(f"Disconnection error: {str(e)}")

    @database_sync_to_async
    def add_online_user(self):
        from django.core.cache import cache
        online_users = cache.get('online_users', set())
        online_users.add(self.user.username)
        cache.set('online_users', online_users)

    @database_sync_to_async
    def remove_online_user(self):
        from django.core.cache import cache
        online_users = cache.get('online_users', set())
        online_users.discard(self.user.username)
        cache.set('online_users', online_users)

    async def broadcast_online_users(self):
        from django.core.cache import cache
        online_users = cache.get('online_users', set())
        await self.channel_layer.group_send(
            'online_users',
            {
                'type': 'online_users_update',
                'users': list(online_users)
            }
        )

    def get_message_model(self):
        return Message