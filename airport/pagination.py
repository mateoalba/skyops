# airport/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginacionEstandar(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limite"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "total": self.page.paginator.count,
            "paginas": self.page.paginator.num_pages,
            "siguiente": self.get_next_link(),
            "anterior": self.get_previous_link(),
            "resultados": data,
        })
# Alias para compatibilidad
StandardPagination = PaginacionEstandar