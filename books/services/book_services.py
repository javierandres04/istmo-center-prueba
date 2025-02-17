from books.serializers.book_serializers import BookSerializer
from books.models import Book
from core.utils.base_crud_service import BaseCrudService


# Utility class to manage book operations
class CrudBookService(BaseCrudService):
    model = Book
    serializer_class = BookSerializer