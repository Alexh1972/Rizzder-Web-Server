import logging

from django.db import models
from .user import User
from ..utils import *

logger = logging.getLogger(__name__)


class UserMatch(models.Model):
    user_match_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    user_first = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, related_name="user_first")
    user_second = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, related_name="user_second")
    date = models.BigIntegerField(default=0)


def getMatch(first, second):
    match = UserMatch.objects.filter(user_first_id=first.user_id,
                                     user_second_id=second.user_id)

    if match.exists():
        return match.get()

    match = UserMatch.objects.filter(user_first_id=second.user_id,
                                     user_second_id=first.user_id)

    if match.exists():
        return match.get()

    return None


def matchUser(first, second):
    if not first.blockedUser(second):
        UserMatch.objects.create(user_first=second, user_second=first, date=currentTimeMillis())
        second.changeScore(50)
        first.changeScore(50)


def unmatchUser(user, receiver, block=False):
    match = getMatch(user, receiver)
    if match is not None:
        from ..messaging import chatName
        from .chat_room import deleteChatRoom, existsChatRoom
        if existsChatRoom(chatName([user, receiver])):
            deleteChatRoom(chatName([user, receiver]))

        match.delete()
        if block:
            user.blockUser(receiver)
