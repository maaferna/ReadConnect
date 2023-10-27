from django.contrib import admin

# Register your models here.
from .models import *


admin.site.site_header = 'READ CONNECT - Books Store'
admin.site.index_title = 'Read Connect'
admin.site.site_title = 'Administrador Django'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'title')
    ordering = ('title', 'pageCount')
    search_fields = ('id', 'title', 'isbn')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(UserBookStatus)
class UserBookStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'currently_reading', 'want_to_read')

@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'rating', 'comment', 'timestamp')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name')