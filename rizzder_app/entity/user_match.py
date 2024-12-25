import logging

from django.db import models
from django.forms import model_to_dict

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

def getMatchesForUser(user):
    matches = UserMatch.objects.filter(user_first_id=user.user_id)

    users = []
    for match in matches.filter():
        match = model_to_dict(match)
        user_first = User.objects.get(user_id=match['user_first'])
        user_second = User.objects.get(user_id=match['user_second'])
        if user.user_id == user_first.user_id:
            user = user_second
        else:
            user = user_first

        users.append(user.serializeUser())

    matches = UserMatch.objects.filter(user_second_id=user.user_id)

    for match in matches.filter():
        match = model_to_dict(match)
        user_first = User.objects.get(user_id=match['user_first'])
        user_second = User.objects.get(user_id=match['user_second'])
        if user.user_id == user_first.user_id:
            user = user_second
        else:
            user = user_first

        users.append(user.serializeUser())

    return users
