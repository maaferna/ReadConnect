from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('books-store/', books_retrieve, name='books_retrieve'),
    path('get_book_details/<int:book_isbn>/', get_book_details, name='get_book_details'),
    path('update_book_status/<str:book_isbn>/', update_book_status, name='update_book_status'),
]