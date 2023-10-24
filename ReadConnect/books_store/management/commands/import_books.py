import os
import json
from django.core.management.base import BaseCommand
from books_store.models import Book, Author, Category
import os

module_dir = os.path.dirname(__file__)
parent_directory = os.path.dirname(module_dir)

class Command(BaseCommand):
    help = 'Import data from a JSON file into the database'

    def handle(self, *args, **kwargs):
        # Construct the full file path to the JSON file
        json_file_path = os.path.join('static', 'datasets', 'amazon.books.json')

        with open(json_file_path, 'r') as file:
            data = json.load(file)

        new_books_count = 0  # Initialize a counter for new books
        # El objetivo de este código es proporcionar una funcionalidad que permita importar datos desde un archivo JSON a una base de datos en una aplicación Django. Está diseñado para ser utilizado como un comando personalizado de administración de Django.
        # En resumen, este código tiene como objetivo importar datos desde un archivo JSON a la base de datos de una aplicación Django. Proporciona una forma robusta de manejar datos con posibles claves faltantes en el JSON, asegurando que el proceso de importación continúe sin problemas y, al final, informa sobre la cantidad de nuevos libros que se agregaron a la base de datos. Esto es especialmente útil para la administración de grandes conjuntos de datos o la actualización periódica de la base de datos de la aplicación.
        for item in data:
            try:
                isbn = item['isbn']
                # Use get() method with a default value to handle missing keys
                title = item.get('title', 'Unknown Title')
                pageCount = item.get('pageCount', 0)
                publishedDate = item.get('publishedDate', {}).get('$date', '2000-01-01T00:00:00.000-0000')
                thumbnailUrl = item.get('thumbnailUrl', '')
                shortDescription = item.get('shortDescription', 'No description available')
                longDescription = item.get('longDescription', 'No description available')
                status = item.get('status', 'PUBLISH')
                authors = item.get('authors', [])
                categories = item.get('categories', [])

                # Check if a book with the same ISBN already exists in the database
                if not Book.objects.filter(isbn=isbn).exists():
                    # Create authors
                    authors = [Author.objects.get_or_create(name=author)[0] for author in authors]

                    # Create categories
                    categories = [Category.objects.get_or_create(name=category)[0] for category in categories]

                    # Create the new book
                    Book.objects.create(
                        title=title,
                        isbn=isbn,
                        pageCount=pageCount,
                        publishedDate=publishedDate,
                        thumbnailUrl=thumbnailUrl,
                        shortDescription=shortDescription,
                        longDescription=longDescription,
                        status=status,
                    )

                    # Add authors and categories to the book
                    book = Book.objects.get(isbn=isbn)
                    book.authors.set(authors)
                    book.categories.set(categories)

                    new_books_count += 1  # Increment the counter
            except KeyError as e:
                # Handle missing key errors by printing an error message and continuing to the next item
                self.stdout.write(self.style.ERROR(f'Error importing book: {str(e)}'))
                continue
        if new_books_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully added {new_books_count} new book(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('No new books added.'))


