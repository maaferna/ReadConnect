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