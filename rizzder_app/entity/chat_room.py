from django.db import models
from django.forms import model_to_dict

from .user import User
from datetime import datetime
from ..utils import currentTimeMillis
import time


class ChatMessage(models.Model):
    chat_message_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    user_sender = models.ManyToManyField(User)
    date = models.BigIntegerField(default=0)
    value = models.CharField(default="", max_length=100000)


class ChatRoom(models.Model):
    chat_room_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    messages = models.ManyToManyField(ChatMessage)
    users = models.ManyToManyField(User)
    name = models.CharField(default="", max_length=10000)


def getChatRooms(user):
    chatRooms = ChatRoom.objects.filter(users=user.user_id)
    chatRooms = [model_to_dict(chatRoom) for chatRoom in chatRooms]

    retChatRooms = []
    for chatRoom in chatRooms:
        retChatRoom = chatRoom
        if len(chatRoom['messages']) is not 0:
            retChatRoom['last_message'] = chatRoom['messages'][-1]
        else:
            retChatRoom['last_message'] = None
        for userChat in chatRoom['users']:
            if userChat.user_id is not user.user_id:
                retChatRoom['user'] = userChat

        del retChatRoom['messages']
        del retChatRoom['users']

        retChatRooms.append(retChatRoom)
    return retChatRooms


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
