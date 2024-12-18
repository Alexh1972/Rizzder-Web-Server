from datetime import timedelta

from django.db import models

from .user_image import UserImage
from django.contrib.auth import get_user_model
import base64
from enum import IntEnum
from django.forms.models import model_to_dict
from ..utils import *


class Gender(IntEnum):
    MAN = 1
    WOMAN = 2


class User(models.Model):
    user_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    username = models.CharField(default="", max_length=1000)
    description_encoded_64 = models.CharField(max_length=10 ** 5, default="")
    birth_date = models.DateField(default="1970-01-01")
    images = models.ManyToManyField(UserImage)
    credential = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, default=None)
    gender = models.IntegerField(Gender, default=Gender.MAN)
    gender_preference = models.IntegerField(Gender, default=Gender.MAN)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    score = models.FloatField(default=1000)
    blocked_users = models.ManyToManyField("self", blank=True, symmetrical=False)

    ### other fields to be added

    def get(self, username=None):
        if username is not None:
            return self.objects.filter(username=username)

        return None

    def changeScore(self, score):
        self.score += score
        self.save()

    def getImagesList(self):
        images = []
        for userImage in self.images.all():
            with open(userImage.image, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                images.append({"image_base_64_encoded": image_data, "id": userImage.user_image_id})

        return images

    def calculateAge(self):
        return calculateYearsPassed(self.birth_date)

    def getPreferredUsers(self, numberOfResults):
        delta = timedelta(days=365 * 10)
        maxDistance = 0.9 * 1  # 0.9 -> 100 km
        users = (User.objects
                 # .filter(gender=self.gender_preference)
                 .exclude(user_id=self.user_id)
                 # maximum distance
                 .filter(longitude__lte=self.longitude + maxDistance)
                 .filter(longitude__gte=self.longitude - maxDistance)
                 .filter(latitude__lte=self.latitude + maxDistance)
                 .filter(latitude__gte=self.latitude - maxDistance)
                 # age difference
                 .filter(birth_date__gte=self.birth_date - delta)
                 # already liked
                 .exclude(user_receiver__user_liker_id=self.user_id)
                 # blocked
                 .exclude(user_id__in=self.blocked_users.all())
                 .exclude(blocked_users__user_id=self.user_id)
                 # already matched
                 .exclude(user_first__user_second_id=self.user_id)
                 .exclude(user_second__user_first_id=self.user_id)
                 .all())

        users = users[0:numberOfResults]
        users = [model_to_dict(user, fields=['user_id', 'username', 'birth_date', 'images', 'description_encoded_64',
                                             'latitude', 'longitude']) for user in users]

        for user in users:
            user['images'] = User.getImagesList(User.objects.get(user_id=user['user_id']))
            user['distance'] = distance(self.latitude, self.longitude, user['latitude'], user['longitude'])
            user['age'] = calculateYearsPassed(user['birth_date'])
            del user['latitude']
            del user['longitude']
            del user['birth_date']
            logger.info(user)
        return users

    def blockUser(self, receiver, changeScore=False):
        # receiver.blocked_users.add(self)
        from ..messaging import disconnectUser, chatName
        self.blocked_users.add(receiver)
        disconnectUser(chatName([self, receiver]), self)
        disconnectUser(chatName([self, receiver]), receiver)
        if changeScore:
            self.changeScore(-100)

    def unblockUser(self, receiver):
        # receiver.blocked_users.remove(self)
        self.blocked_users.remove(receiver)

        if not self.blockedUser(receiver):
            from ..messaging import connectUser, chatName
            connectUser(chatName([self, receiver]), self)
            connectUser(chatName([self, receiver]), receiver)

    def blockedUser(self, user):
        return (self.blocked_users.filter(user_id=user.user_id).exists() or
                user.blocked_users.filter(user_id=self.user_id).exists())

    def canChat(self, user):
        from .user_match import getMatch
        if not self.blockedUser(user) and getMatch(self, user) is not None:
            return True

        return False
