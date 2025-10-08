from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Custom pagination with configurable page_size via query param"""

    page_size = 20  # Default
    page_size_query_param = "page_size"  # Allow client to set page_size
    max_page_size = 100  # Maximum limit
