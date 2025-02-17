from books.serializers.book_serializers import BookSerializer
from books.services.book_services import BookService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
    def get(self, request):
        books = BookService.get_books()

        result_page = self.paginator.paginate_queryset(books, request)

        serializer = BookSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    # Create a book
    def post(self, request):
        data = request.data
        book = BookService.create_book(data)
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
    def get(self, request, id):
        book = BookService.get_book_by_id(id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # Update a book
    def put(self, request, id):
        data = request.data
        book = BookService.update_book(id, data)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # Partial update a book
    def patch(self, request, id):
        data = request.data
        book = BookService.update_book(id, data, partial=True)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # Delete a book
    def delete(self, request, id):
        book = BookService.delete_book(id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
