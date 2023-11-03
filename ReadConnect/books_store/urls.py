from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"books_currently_reading", UserBookStatusViewSet, basename="wants")

urlpatterns = [
    path('', index, name='home'),
    path('books-store/', books_retrieve, name='books_retrieve'),
    path('get_book_details/<str:book_isbn>/', get_book_details, name='get_book_details'),
    path('read_connect_books/', read_connect_books, name='read_connect_books'),
    path('update_book_status/<str:book_isbn>/', update_book_status, name='update_book_status'),
    path('create_book_rating/<str:book_id>/', create_book_rating, name='create_book_rating'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('user_profile/', profile, name='user_profile'),
    path('want-to-read-books/', WantToReadBooksView.as_view(), name='want_to_read_books'),
    path('api-books/', include(router.urls)),
    path('api/dashboard-data/', DashboardData.as_view(), name='dashboard-data'),
    path('api/get-user-profile/', get_user_profile, name='get_user_profile'),
]