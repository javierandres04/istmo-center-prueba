

from users.serializers import UserSerializer
from .models import User
from rest_framework.exceptions import ValidationError, NotFound


# Utility class to manage user operations
class UserService:
    @staticmethod
    def create_user(data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return user
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def get_users():
        return User.objects.all()

    @staticmethod
    def get_user_by_username(username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User not found.")
    
    @staticmethod
    def update_user(username, data, partial=False):
        user = UserService.get_user_by_username(username)
        serializer = UserSerializer(user, data=data, partial=partial)
        if serializer.is_valid():
          user = serializer.save()
          return user
        else:
            raise ValidationError(serializer.errors)
    
    @staticmethod
    def delete_user(username):
        user = UserService.get_user_by_id(username)
        user.delete()
        return user