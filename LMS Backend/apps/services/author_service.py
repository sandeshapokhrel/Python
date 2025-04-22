from django.shortcuts import get_object_or_404
from apps.core.models import Author
from typing import List, Optional

def list_authors() -> List[Author]:
    """Returns a list of all authors."""
    return Author.objects.all()

def get_author_by_id(author_id: int) -> Author:
    """
    Retrieves a single author by their ID.
    Raises Http404 if not found.
    """
    return get_object_or_404(Author, pk=author_id)

def create_author(name: str, birth_date: Optional[str] = None, biography: Optional[str] = None) -> Author:
    """
    Creates a new author.

    Args:
        name (str): The name of the author.
        birth_date (Optional[str]): The birth date (YYYY-MM-DD).
        biography (Optional[str]): A short biography.

    Returns:
        Author: The newly created author object.
    """
    # Basic validation could be added here if needed,
    # but DRF serializers will handle most input validation.
    author = Author.objects.create(
        name=name,
        birth_date=birth_date,
        biography=biography
    )
    return author

def update_author(author_id: int, name: str, birth_date: Optional[str] = None, biography: Optional[str] = None) -> Author:
    """
    Updates an existing author.

    Args:
        author_id (int): The ID of the author to update.
        name (str): The updated name.
        birth_date (Optional[str]): The updated birth date.
        biography (Optional[str]): The updated biography.

    Returns:
        Author: The updated author object.
    """
    author = get_author_by_id(author_id)
    author.name = name
    author.birth_date = birth_date
    author.biography = biography
    author.save()
    return author

def delete_author(author_id: int) -> None:
    """
    Deletes an author by their ID.
    """
    author = get_author_by_id(author_id)
    # Consider implications: What happens to books by this author?
    # Current Book model uses on_delete=models.SET_NULL for author FK.
    author.delete()