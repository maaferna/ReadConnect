from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('books-store/', books_retrieve, name='books_retrieve'),
    path('get_book_details/<int:book_id>/', get_book_details, name='get_book_details'),
]