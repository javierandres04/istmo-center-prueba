

from ..models import User
from core.utils.base_crud_service import BaseCrudService
from users.serializers.user_serializers import UserSerializer, SimpleUserSerializer


class UserService(BaseCrudService):
    model = User
    serializer_class = UserSerializer

    # Need to override create method to hash password
    @classmethod
    def create(self, data):
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = User(
                email=serializer.validated_data['email'],
                name=serializer.validated_data['name'],
                role=serializer.validated_data['role']
            )

            user.set_password(serializer.validated_data['password'])
            user.save()

            return serializer.data

    # Need to override update method to hash password
    @classmethod
    def update(self, id, data, partial=False):
        user = UserService.get_by_id(id)
        serializer = self.serializer_class(user, data=data, partial=partial)
        if serializer.is_valid(raise_exception=True):
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
            user.save()
            return user

    # Added method to register a simple user
    @staticmethod
    def register_user(data):
        serializer = SimpleUserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = User(
                email=serializer.validated_data['email'],
                name=serializer.validated_data['name']
            )

            user.set_password(serializer.validated_data['password'])
            user.save()

            return serializer.data
