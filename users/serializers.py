from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "name", "role"]
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "password"]
        extra_kwargs = {'password': {'write_only': True}}
  

