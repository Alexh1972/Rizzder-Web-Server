from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', user_registration.as_view(), name='register'),
    path('api/user/edit/', views.userEdit, name='editUser'),
    path('api/user/edit/photo/', views.userEditPhoto, name='editUserPhoto'),
    path('api/user/edit/delete/photo/', views.userDeletePhoto, name='deleteUserPhoto'),
    path('api/user/getPreferredUsers/', views.getPreferredUsers, name='getPreferredUsers'),
    path('api/user/genders/', views.getGenders, name='getGenders'),
    path('api/user/info/getLocation/', views.getUserLocation, name='getUserLocation'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('user/meet/', views.userMeetView, name='userMeetView'),
    path('user/edit/', views.userEditView, name='editUserView'),
]
