from rest_framework.pagination import PageNumberPagination

class RunPagination(PageNumberPagination):
    page_size_query_param = 'size'

class UserPagination(PageNumberPagination):
    page_size_query_param = 'size'
