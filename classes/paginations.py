from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 6

class TrainerPagination(PageNumberPagination):
    page_size = 8