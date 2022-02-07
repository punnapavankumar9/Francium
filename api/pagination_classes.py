from rest_framework.pagination import PageNumberPagination


class LargeResultSetPaginator(PageNumberPagination):
    page_size = 100


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


class TestingResultsSetPagination(PageNumberPagination):
    page_size = 1
