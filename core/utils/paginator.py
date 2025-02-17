from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# Custom pagination class for the entire API
class customResultsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'total_records': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
