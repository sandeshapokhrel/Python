from django.db import models
from .author import Author # Import the Author model

class Book(models.Model):
    """
    Represents a book in the library.
    """
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, help_text='13 Character ISBN')
    published_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    stock = models.PositiveIntegerField(default=0, help_text='Number of available copies')

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title'] # Optional: Order books alphabetically by title