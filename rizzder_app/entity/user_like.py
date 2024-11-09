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
    like = models.BooleanField(default=False)
    date = models.DateField(default="1970-01-01")

    def get(self, user_receiver):
        if user_receiver is not None:
            return self.objects.filter(user_receiver__user_id=user_receiver.user_id)

        return None


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
