from books.serializers.book_serializers import BookLoanSerializer
from books.services.book_services import loanBookService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.decorators.views_error_handling import handle_view_exceptions
from core.utils.paginator import customResultsPagination


class ListCreateLoans(APIView):
    paginator = customResultsPagination()
    permission_classes = [IsAuthenticated]

    # Get all user loans
    @handle_view_exceptions
    def get(self, request):
        user = request.user
        loans = loanBookService.get_loans_by_user(user.id)

        result_page = self.paginator.paginate_queryset(loans, request)
        serializer = BookLoanSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    # Create a loan
    @handle_view_exceptions
    def post(self, request):
        data = request.data
        user = request.user
        book_loan = loanBookService.loan_book(data['book_id'], user.id)
        serializer = BookLoanSerializer(book_loan)
        if book_loan:
            return Response({'message': 'Book loan successfully created', 'detail': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)


class ReturnBook(APIView):
    permission_classes = [IsAuthenticated]

    # Return a book
    @handle_view_exceptions
    def post(self, request):
        data = request.data
        user = request.user
        book_loan = loanBookService.return_book(data['book_id'], user.id)
        serializer = BookLoanSerializer(book_loan)
        if book_loan:
            return Response({'message': 'Book returned', 'detail': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Book not loaned to user'}, status=status.HTTP_400_BAD_REQUEST)