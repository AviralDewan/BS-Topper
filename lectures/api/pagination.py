from rest_framework.pagination import PageNumberPagination

class TimeStampPaginator(PageNumberPagination):
    page_size = 10
