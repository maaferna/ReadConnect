from django.db import models

# Create your models here.

from django.db import models

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

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name