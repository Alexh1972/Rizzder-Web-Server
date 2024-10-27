import jwt
from ..models import User
import logging
from django.contrib.auth.models import User as authUser

logger = logging.getLogger(__name__)

class JWTTokenDecoder():
    token = ""

    def __init__(self, token):
        self.token = token

    def getUserFromToken(self):
        decodedPayload = jwt.decode(self.token, None, None)
        user_id = decodedPayload.get("user_id")
        auth_user = authUser.objects.get(id=user_id)

        return User.objects.get(username=auth_user.username)
