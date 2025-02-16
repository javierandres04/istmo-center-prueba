from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

def handle_view_exceptions(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            return func(self, request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"error": e.detail}, status=status.HTTP_404_NOT_FOUND)
        #except Exception as e:
 #           return Response({"error": f"An unexpected error occour"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper