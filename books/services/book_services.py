from books.serializers.book_serializers import BookSerializer
from books.models import Book
from rest_framework.exceptions import ValidationError, NotFound


# Utility class to manage book operations
class BookService:
    @staticmethod
    def create_book(data):
      serializer = BookSerializer(data=data)
      if serializer.is_valid():
        serializer.save()
        return serializer.data
      else:
          raise ValidationError(serializer.errors)

    @staticmethod
    def get_books():
      return Book.objects.all()

    @staticmethod
    def get_book_by_id(id):
      try:
          return Book.objects.get(id=id)
      except Book.DoesNotExist:
          raise NotFound("book not found.")

    @staticmethod
    def update_book(id, data, partial=False):
      book = BookService.get_book_by_id(id)
      serializer = BookSerializer(book, data=data, partial=partial)
      if serializer.is_valid():
        serializer.save()
        return book
      else:
        raise ValidationError(serializer.errors)

    @staticmethod
    def delete_book(id):
        book = BookService.get_book_by_id(id)
        book.delete()
        return book
    