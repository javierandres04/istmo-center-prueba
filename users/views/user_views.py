from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers.user_serializers import UserSerializer, SimpleUserSerializer
from users.services.user_services import UserService
from core.decorators.views_error_handling import handle_view_exceptions
from core.utils.paginator import customResultsPagination


# Class based view used to create and list all the users
class listCreateUsersView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    paginator = customResultsPagination()

    # Get All Users
    @handle_view_exceptions
    def get(self, request):
        users = UserService.get_all()

        result_page = self.paginator.paginate_queryset(users, request)

        serializer = UserSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    # Create User
    @handle_view_exceptions
    def post(self, request):
        data = request.data
        user = UserService.create(data)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Class based view used to retrieve, update and delete an specific user
class retrieveUpdateDeleteUserView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    # get user by id
    @handle_view_exceptions
    def get(self, request, id):
        user = UserService.get_by_id(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # Update complete User
    @handle_view_exceptions
    def put(self, request, id):
        data = request.data
        user = UserService.update(id, data)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # Update partial User
    @handle_view_exceptions
    def patch(self, request, id):
        data = request.data
        user = UserService.update(id, data, partial=True)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # delete user
    @handle_view_exceptions
    def delete(self, request, id):
        user = UserService.delete(id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

# Class based view used to register a new user without admin permissions
class registerUserView(APIView):
    permission_classes = [AllowAny]

    @handle_view_exceptions
    def post(self, request):
        data = request.data
        user = UserService.register_user(data)
        serializer = SimpleUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
