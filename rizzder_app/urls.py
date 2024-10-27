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
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('user/edit', views.userEditView, name='editUserView'),
    path('home/', views.home, name='home'),
]
