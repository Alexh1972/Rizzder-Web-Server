from django.db import models
from .user import User
from datetime import datetime
from ..utils import currentTimeMillis
import time


class ChatMessage(models.Model):
    chat_message_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    user_sender = models.ManyToManyField(User)
    date = models.BigIntegerField(default=currentTimeMillis())
    value = models.CharField(default="", max_length=100000)


class ChatRoom(models.Model):
    chat_room_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    messages = models.ManyToManyField(ChatMessage)
    users = models.ManyToManyField(User)
    name = models.CharField(default="", max_length=10000)


def getChatRoom(name):
    chatRoom = ChatRoom.objects.filter(name=name)

    if not chatRoom.exists():
        return None, []

    chatRoom = chatRoom.get()
    messages = chatRoom.messages.all()
    return chatRoom, messages


def existsChatRoom(name):
    chatRoom = ChatRoom.objects.filter(name=name)

    return chatRoom.exists()


def deleteChatRoom(name):
    chatRoom = ChatRoom.objects.get(name=name)
    for message in chatRoom.messages.all():
        for user_sender in message.user_sender.all():
            user_sender.delete()
        message.delete()
    chatRoom.delete()
