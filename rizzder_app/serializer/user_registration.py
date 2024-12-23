from rest_framework import serializers
from django.contrib.auth.models import User


class user_registration_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        labels = {
            'username': 'Enter your Username',
            'password': 'Create a Password',
            'email': 'Enter your Email',
        }

    def create(self, validated_data):
        data = User.objects.create_user(**validated_data)
        return data
