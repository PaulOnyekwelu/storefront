from rest_framework.pagination import PageNumberPagination


class DefaultStorePagination(PageNumberPagination):
    page_size = 100
