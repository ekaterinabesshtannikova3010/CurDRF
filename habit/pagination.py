from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Настройка пагинации
    """
    page_size = 5  # Количество элементов на странице
    page_size_query_param = "page_size"  # Позволяет клиенту задавать размер страницы
    max_page_size = 50  # Максимально допустимый размер страницы

    def get_paginated_response(self, data):
        return Response(
            {
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next_page": self.get_next_link(),
                "previous_page": self.get_previous_link(),
                "results": data,
            }
        )
