from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat between {', '.join(user.username for user in self.participants.all())}"

    @staticmethod
    def get_or_create_room(user1, user2):
        # Sort users to ensure consistent room names
        users = sorted([user1, user2], key=lambda user: user.username)
        room_name = f"chat_{users[0].username}_{users[1].username}"
        
        room, created = Room.objects.get_or_create(name=room_name)
        if created:
            room.participants.add(user1, user2)
        
        return room

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"