from django.db import models
from .user_image import UserImage
from django.contrib.auth import get_user_model
import base64
from datetime import date
from enum import IntEnum

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
        today = date.today()
        return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

