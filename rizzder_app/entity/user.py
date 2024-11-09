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

    ### other fields to be added

    def get(self, username=None):
        if username is not None:
            return self.objects.filter(username=username)

        return None

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
        from . import UserLike
        users = (User.objects
                 .filter(gender=self.gender_preference)
                 .exclude(user_id=self.user_id)
                 # TODO check if results are not returned twice (table containing user_id_recv -> user_id_ret)
                 .all())
        users = [user for user in users if abs(self.calculateAge() - calculateYearsPassed(user.birth_date) < 10)]
        users = [user for user in users if
                 not UserLike.objects.filter(user_receiver__user_id=user.user_id, user_liker__user_id=self.user_id).exists()]
        users = users[0:numberOfResults]
        users = [model_to_dict(user, fields=['user_id', 'username', 'birth_date', 'images', 'description_encoded_64', 'latitude', 'longitude']) for user in users]

        for user in users:
            user['images'] = User.getImagesList(User.objects.get(user_id=user['user_id']))
            user['distance'] = distance(self.latitude, self.longitude, user['latitude'], user['longitude'])
            del user['latitude']
            del user['longitude']
            logger.info(user)
        return users
