import logging

from django.db import models

from .user import User
from ..utils import *
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class UserLike(models.Model):
    user_like_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    user_liker = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, related_name="user_liker")
    user_receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, related_name="user_receiver")
    # like = True (possible matching), like = False (blocked)
    like = models.BooleanField(default=False)
    date = models.DateField(default="1970-01-01")

    def get(self, user_receiver):
        if user_receiver is not None:
            return self.objects.filter(user_receiver__user_id=user_receiver.user_id)

        return None


def addUserLike(liker, receiver):
    if userLikeExists(liker=receiver, receiver=liker):
        deleteUserLike(receiver, liker)
        liker.changeScore(50)
        receiver.changeScore(50)
        return True
    UserLike.objects.create(user_liker=liker,
                            user_receiver=receiver,
                            like=True,
                            date=date.today())
    return False


def addUserDislike(disliker, receiver, subtractScore=True):
    if not userLikeExists(liker=disliker, receiver=receiver, like=False):
        if subtractScore:
            disliker.changeScore(-100)
        UserLike.objects.create(user_liker=disliker,
                                user_receiver=receiver,
                                like=False,
                                date=date.today())


def userLikeExists(liker, receiver, like=True):
    return UserLike.objects.get(user_liker__user_id=liker.user_id,
                                user_receiver__user_id=receiver.user_id,
                                like=like)


def deleteUserLike(liker, receiver):
    UserLike.objects.get(user_liker__user_id=liker.user_id,
                         user_receiver__user_id=receiver.user_id).delete()


from apscheduler.schedulers.background import BackgroundScheduler


def cleanOldLikes():
    minDate = datetime.now() - timedelta(days=7)

    logger.info("Deleting UserLikes older than " + str(minDate))
    UserLike.objects.filter(date__lte=minDate).delete()


def start():
    logger.info("Starting job - name : Clean Old Likes")
    scheduler = BackgroundScheduler()

    scheduler.add_job(cleanOldLikes, 'interval', days=1, next_run_time=datetime.now() + timedelta(seconds=10))
    scheduler.start()
