from django.db import models
from .user_image import UserImage
from django.contrib.auth import get_user_model
import base64


class User(models.Model):
    user_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    username = models.CharField(default="", max_length=1000)
    description_encoded_64 = models.CharField(max_length=10 ** 5, default="")
    birth_date = models.DateField(default="1970-01-01")
    # images = models.ForeignKey(UserImage, on_delete=models.CASCADE)
    credential = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)

    ### other fields to be added

    def get(self, username=None):
        if username is not None:
            return self.objects.filter(username=username)

        return None
