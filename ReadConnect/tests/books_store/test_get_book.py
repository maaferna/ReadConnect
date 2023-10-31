from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from books_store.models import Book

class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user for authentication
        self.user = User.objects.create_user(
            username='user2',
            password='claveuser'
        )

    def test_get_book_by_isbn_authenticated(self):
        # ISBN to filter by
        isbn = "1884777902"

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Perform a GET request to retrieve the book by ISBN
        response = self.client.get(f"/books/?isbn={isbn}")

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the retrieved book's ISBN matches the expected ISBN
        data = response.data
        self.assertEqual(data[0]['isbn'], isbn)

    def test_get_book_by_isbn_unauthenticated(self):
        # ISBN to filter by
        isbn = "1884777902"

        # Perform a GET request to retrieve the book by ISBN without authentication
        response = self.client.get(f"/books/?isbn={isbn}")

        # Check if the response status code is 403 (Forbidden) for unauthenticated users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



