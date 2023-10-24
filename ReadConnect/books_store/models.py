from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    pageCount = models.PositiveIntegerField()
    publishedDate = models.DateTimeField()
    thumbnailUrl = models.URLField(max_length=255)
    shortDescription = models.TextField()
    longDescription = models.TextField()
    status = models.CharField(max_length=10, choices=[
        ('PUBLISH', 'Publish'),
        ('MEAP', 'Meap'),
    ])
    authors = models.ManyToManyField('Author', related_name='books')
    categories = models.ManyToManyField('Category', related_name='books')

    def __str__(self):
        return self.title


class UserBookStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    currently_reading = models.BooleanField(default=False)
    want_to_read = models.BooleanField(default=False)
    def __str__(self):
        return f"Status for {self.user.username} on {self.book.title}"


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
