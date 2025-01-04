import jwt
import logging
from django.contrib.auth.models import User as authUser
from django.conf import settings

logger = logging.getLogger(__name__)

class JWTTokenDecoder():
    token = ""

    def __init__(self, request):
        if 'token' in request.POST:
            self.token = request.POST['token']
        else:
            self.token = request.GET['token']

    def getUserFromToken(self):
        from ..models import User
        from rizzder_app.utils import currentTimeMillis
        decodedPayload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decodedPayload.get("user_id")
        auth_user = authUser.objects.get(id=user_id)
        user = User.objects.get(username=auth_user.username)

        if user is not None:
            user.last_online = currentTimeMillis()
            user.save()
        return user
