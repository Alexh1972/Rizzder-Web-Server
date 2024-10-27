from django.db import models


class UserImage(models.Model):
    user_image_id = models.BigIntegerField(primary_key=True, default=0)
    image = models.ImageField(default="")
    active = models.BooleanField(default=False)

    def __init__(self, image, active):
        self.image = image
        self.active = active