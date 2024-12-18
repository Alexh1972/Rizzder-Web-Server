from django.urls import path
from . import view
from .view import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', user_registration.as_view(), name='register'),
    path('api/user/edit/', view.userEdit, name='editUser'),
    path('api/user/edit/photo/', view.userEditPhoto, name='editUserPhoto'),
    path('api/user/edit/delete/photo/', view.userDeletePhoto, name='deleteUserPhoto'),
    path('api/user/getPreferredUsers/', view.getPreferredUsers, name='getPreferredUsers'),
    path('api/user/genders/', view.getGenders, name='getGenders'),
    path('api/user/meet/like/', view.likeUser, name='likeUser'),
    path('api/user/block/', view.blockUser, name='blockUser'),
    path('api/user/unblock/', view.unblockUser, name='unblockUser'),
    path('api/user/info/getLocation/', view.getUserLocation, name='getUserLocation'),
    path('api/user/setGhosted/', view.setGhosted, name='setGhosted'),
    path('login/', view.login, name='login'),
    path('signup/', view.signup, name='signup'),
    path('home/', view.home, name='home'),
    path('', home, name='home'),
    path('user/meet/', view.userMeetView, name='userMeetView'),
    path('user/edit/', view.userEditView, name='editUserView'),
    path('user/chatRoom/', view.chatRoomView, name='chatRoom'),
]
