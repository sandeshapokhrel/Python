from django.shortcuts import get_object_or_404
from apps.core.models import Book, Author
from typing import List, Optional

def list_books() -> List[Book]:
    """Returns a list of all books."""
    # Use select_related to optimize fetching the related author
    return Book.objects.select_related('author').all()

def get_book_by_id(book_id: int) -> Book:
    """
    Retrieves a single book by its ID.
    Raises Http404 if not found.
    """
    # Use select_related to optimize fetching the related author
    return get_object_or_404(Book.objects.select_related('author'), pk=book_id)

def create_book(title: str, isbn: str, stock: int, author_id: Optional[int] = None, published_date: Optional[str] = None) -> Book:
    """
    Creates a new book.

    Args:
        title (str): The title of the book.
        isbn (str): The unique ISBN.
        stock (int): The number of available copies.
        author_id (Optional[int]): The ID of the author.
        published_date (Optional[str]): The publication date (YYYY-MM-DD).

    Returns:
        Book: The newly created book object.

    Raises:
        Author.DoesNotExist: If the author_id is provided but invalid.
        IntegrityError: If the ISBN is not unique.
    """
    author = None
    if author_id:
        # Ensure the author exists before creating the book
        author = get_object_or_404(Author, pk=author_id) # Use get_object_or_404 for clarity

    book = Book.objects.create(
        title=title,
        isbn=isbn,
        published_date=published_date,
        author=author,
        stock=stock
    )
    return book

def update_book(book_id: int, title: str, isbn: str, stock: int, author_id: Optional[int] = None, published_date: Optional[str] = None) -> Book:
    """
    Updates an existing book.

    Args:
        book_id (int): The ID of the book to update.
        title (str): The updated title.
        isbn (str): The updated ISBN.
        stock (int): The updated stock count.
        author_id (Optional[int]): The updated author ID.
        published_date (Optional[str]): The updated publication date.

    Returns:
        Book: The updated book object.

    Raises:
        Author.DoesNotExist: If the author_id is provided but invalid.
        IntegrityError: If the updated ISBN conflicts with another book.
    """
    book = get_book_by_id(book_id) # Fetches the book
    author = None
    if author_id:
        author = get_object_or_404(Author, pk=author_id)

    book.title = title
    book.isbn = isbn
    book.published_date = published_date
    book.author = author
    book.stock = stock
    book.save()
    return book

def delete_book(book_id: int) -> None:
    """
    Deletes a book by its ID.
    """
    book = get_book_by_id(book_id)
    # Consider implications: What if the book is currently borrowed?
    # The Transaction model uses on_delete=models.PROTECT for the book FK,
    # so deleting a borrowed book will raise ProtectedError. This is intended.
    book.delete()