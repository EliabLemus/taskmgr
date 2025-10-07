"""
Custom pagination classes for Task Manager API
"""
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination that allows client to set page size via query param
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
