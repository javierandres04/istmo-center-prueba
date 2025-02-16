

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
    def get_user_by_id(id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound("User not found.")
    
    @staticmethod
    def update_user(id, data, partial=False):
        user = UserService.get_user_by_id(id)
        serializer = UserSerializer(user, data=data, partial=partial)
        if serializer.is_valid():
          user = serializer.save()
          return user
        else:
            raise ValidationError(serializer.errors)
    
    @staticmethod
    def delete_user(id):
        user = UserService.get_user_by_id(id)
        user.delete()
        return user