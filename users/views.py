from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
from users.user_services import UserService


# Class based view used to create and list all the users
class listCreateUsersView(APIView):
  #Get All Users
  def get(self, request):
    users = UserService.get_users()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
  
  def post(self, request):
    data = request.data
    try:
        user = UserService.create_user(data)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response("An error occour while creating the usar", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Class based view used to retrieve, update and delete an specific user
class retrieveUpdateDeleteUserView(APIView):
  #get user by username
  def get(self, request, username):
    try:
        user = UserService.get_user_by_username(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except NotFound as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response("An error occour while retrieving the user", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  # Update complete User
  def put(self, request, username):
    data = request.data
    try:
        user = UserService.update_user(username, data)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except NotFound as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response("An error occour while updating the user", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
  # Update partial User
  def patch(self, request, username):
    data = request.data
    try:
        user = UserService.update_user(username, data, partial=True)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except NotFound as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response("An error occour while updating the user", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  # delete user
  def delete(self, request, username):
    try:
        user = UserService.delete_user(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except NotFound as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response("An error occour while deleting the user", status=status.HTTP_500_INTERNAL_SERVER_ERROR)