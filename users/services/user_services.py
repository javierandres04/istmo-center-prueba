

from users.serializers.user_serializers import UserSerializer, SimpleUserSerializer
from ..models import User
from rest_framework.exceptions import ValidationError, NotFound


# Utility class to manage user operations
class UserService:
    @staticmethod
    def create_user(data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = User(
                email=serializer.validated_data['email'],
                name=serializer.validated_data['name'],
                role=serializer.validated_data['role']
            )

            user.set_password(serializer.validated_data['password'])
            user.save()

            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    def register_user(data):
        serializer = SimpleUserSerializer(data=data)
        if serializer.is_valid():
            user = User(
                email=serializer.validated_data['email'],
                name=serializer.validated_data['name']
            )

            user.set_password(serializer.validated_data['password'])
            user.save()

            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def get_users():
        return User.objects.all().order_by('id')

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
            if partial:
                user.email = serializer.validated_data.get('email', user.email)
                user.name = serializer.validated_data.get('name', user.name)
                user.role = serializer.validated_data.get('role', user.role)
                user.set_password(serializer.validated_data.get(
                    'password', user.password))
            else:
                user.email = serializer.validated_data['email']
                user.name = serializer.validated_data['name']
                user.role = serializer.validated_data['role']
                user.set_password(serializer.validated_data['password'])

            return user
        else:
            raise ValidationError(serializer.errors)

    @staticmethod
    def delete_user(id):
        user = UserService.get_user_by_id(id)
        user.delete()
        return user
