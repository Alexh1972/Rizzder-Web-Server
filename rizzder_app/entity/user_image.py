from django.db import models

class UserImage(models.Model):
    user_image_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    image = models.CharField(default="", max_length=1000)
    active = models.BooleanField(default=False)
