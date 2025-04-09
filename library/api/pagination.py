from rest_framework.pagination import PageNumberPagination

class ResourcePaginator(PageNumberPagination):
    page_size = 10
