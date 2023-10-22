from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('books_store/', books_retrieve, name='books_retrieve'),
]