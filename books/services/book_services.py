from datetime import datetime
from books.serializers.book_serializers import BookSerializer
from books.models import Book, BookLoan
from core.utils.base_crud_service import BaseCrudService
from django.db import transaction
from rest_framework.exceptions import NotFound



# Utility class to manage book operations
class CrudBookService(BaseCrudService):
    model = Book
    serializer_class = BookSerializer


# Utility class to manage book loan operations
class loanBookService():
    @staticmethod
    def get_loans_by_user(user_id):
       return BookLoan.objects.filter(user_id=user_id).all().order_by('loan_date')

    @staticmethod
    def loan_book(book_id, user_id):
        book_loan = None
        # Create a transaction to ensure that the book is not loaned to two users at the same time
        with transaction.atomic():
            book = Book.objects.select_for_update().filter(id=book_id).first()
            if book: # Lock the book row
                if book.available:
                    book.available = False
                    book.save()
                    book_loan = BookLoan.objects.create(
                        book=book,
                        user_id=user_id,
                    )
            else :
                 raise NotFound(f"Book not found.")
                
        return book_loan
    
    @staticmethod
    def return_book(book_id, user_id):
        book_loan = False
        with transaction.atomic():
            book = Book.objects.select_for_update().filter(id=book_id).first()
            if book:
                book_loan = BookLoan.objects.select_for_update().filter(book_id=book_id, user_id=user_id, returned=False).first()
                if book_loan:
                    book.available = True
                    book.save()

                    book_loan.returned = True
                    book_loan.return_date = datetime.now()
                    book_loan.save()
                    
                else:
                    raise NotFound(f"Book not loaned to user.")
            else:
                raise NotFound(f"Book not found.")
        
        return book_loan