# This file makes the 'models' directory a Python package.

# Import models here to make them easily accessible
from .author import Author
from .book import Book
from .student import Student
from .transaction import Transaction

# Define __all__ for explicit public interface (optional but good practice)
__all__ = ['Author', 'Book', 'Student', 'Transaction']