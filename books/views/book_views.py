from books.serializers.book_serializers import BookSerializer
from books.services.book_services import CrudBookService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.decorators.views_error_handling import handle_view_exceptions
from core.utils.paginator import customResultsPagination


class ListCreateBooksView(APIView):
    paginator = customResultsPagination()

    def get_permissions(self):
        # Mapping Django rest framework permissions according to the method
        permission_classes = {
            'GET': [IsAuthenticated()],
            'POST': [IsAuthenticated(), IsAdminUser()],
        }
        # Return the permissions for the current request method
        return permission_classes.get(self.request.method,  [IsAuthenticated(), IsAdminUser()])

    # Get all books
    @handle_view_exceptions
    def get(self, request):
        books = CrudBookService.get_all()

        result_page = self.paginator.paginate_queryset(books, request)

        serializer = BookSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    # Create a book
    @handle_view_exceptions
    def post(self, request):
        data = request.data
        book = CrudBookService.create(data)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class retrieveUpdateDeleteBookView(APIView):
    # Only Admin users can modify books
    def get_permissions(self):
        permission_classes = {
            'GET': [IsAuthenticated()],
            'PUT': [IsAuthenticated(), IsAdminUser()],
            'PATCH': [IsAuthenticated(), IsAdminUser()],
            'DELETE': [IsAuthenticated(), IsAdminUser()],
        }
        return permission_classes.get(self.request.method,  [IsAuthenticated(), IsAdminUser()])

    # Get a book by id
    @handle_view_exceptions
    def get(self, request, id):
        book = CrudBookService.get_by_id(id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # Update a book
    @handle_view_exceptions
    def put(self, request, id):
        data = request.data
        book = CrudBookService.update(id, data)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # Partial update a book
    @handle_view_exceptions
    def patch(self, request, id):
        data = request.data
        book = CrudBookService.update(id, data, partial=True)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # Delete a book
    @handle_view_exceptions
    def delete(self, request, id):
        book = CrudBookService.delete(id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
