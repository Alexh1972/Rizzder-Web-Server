from django.db import models
from .user_image import UserImage


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True, default=0)
    name = models.CharField(max_length=100, default="")
    description_encoded_64 = models.CharField(max_length=10 ** 5, default="")
    birth_date = models.DateField(default="1970-01-01")
    images = models.ForeignKey(UserImage, on_delete=models.CASCADE)
    ### other fields to be added
