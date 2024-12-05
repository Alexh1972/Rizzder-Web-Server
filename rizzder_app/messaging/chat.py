import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.roomGroupName = None

    async def connect(self):
        from ..models import ChatRoom, User
        self.roomGroupName = self.scope['url_route']['kwargs']['room_name']
        users = usersFromChatName(self.roomGroupName)
        if len(users) == 2:
            firstUser = User.objects.get(user_id=users[0])
            secondUser = User.objects.get(user_id=users[1])

            if firstUser.blockedUser(secondUser):
                await self.close()

        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

        if not ChatRoom.objects.filter(name=self.roomGroupName).exists():
            chatRoom = ChatRoom.objects.create(name=self.roomGroupName)
            for user_id in users:
                chatRoom.users.add(User.objects.get(user_id=user_id))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data=None, bytes_data=None):
        from ..models import ChatMessage, ChatRoom, User
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        userId = text_data_json["userId"]
        time = text_data_json["time"]

        chatRoom = ChatRoom.objects.get(name=self.roomGroupName)
        chatMessage = ChatMessage.objects.create(date=time, value=message)
        chatMessage.save()
        chatMessage.user_sender.add(User.objects.get(user_id=userId))

        chatRoom.messages.add(chatMessage)

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "userId": userId,
                "time": time
            })

    async def sendMessage(self, event):
        message = event["message"]
        userId = event["userId"]
        time = event["time"]

        await self.send(text_data=json.dumps({"message": message, "userId": userId, "time": time}))


delimiter = '$'

def chatName(users):
    from ..models import User
    if len(users) == 0:
        return None

    s = ""
    users = sorted(users, key=lambda x: x.user_id, reverse=False)
    idx = 0
    for user in users:
        s += str(user.user_id)
        idx += 1
        if idx != len(users):
            s += delimiter

    return base64.b16encode(bytes(s, "utf-8")).decode("ascii")


def usersFromChatName(chatName):
    string = base64.b16decode(chatName).decode("ascii")
    return string.split(delimiter)
