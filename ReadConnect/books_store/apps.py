from django.apps import AppConfig


class BooksStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books_store'
    def ready(self):
        import books_store.signals  # Import the signals module to connect the signal handler