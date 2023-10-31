from books_store.models import *
import pytest
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.mark.django_db
def test_create_book():
    author = Author.objects.create(name="Author Name")
    book = Book.objects.create(
        title="Sample Book",
        isbn="1234567890123",
        pageCount=200,
        publishedDate="2023-10-01T00:00:00.000-0700",
        thumbnailUrl="http://example.com/thumbnail.jpg",
        shortDescription="Short description",
        longDescription="Long description",
        status="PUBLISH",
    )
    book.authors.add(author)

    assert Book.objects.count() == 1

# Add more tests for models
