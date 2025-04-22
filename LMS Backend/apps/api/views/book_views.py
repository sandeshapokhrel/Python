from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.core.models import Book
from ..serializers.book_serializers import BookSerializer
from apps.services import book_service # Import the service functions

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    Uses the BookService for business logic.
    """
    queryset = Book.objects.select_related('author').all().order_by('title') # Optimize query
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Override standard methods to use the service layer

    def perform_create(self, serializer):
        """Calls the service layer to create a book."""
        validated_data = serializer.validated_data
        # Extract author instance if author_id was provided
        author = validated_data.pop('author', None) # source='author' maps author_id to author instance
        author_id = author.pk if author else None
        book_service.create_book(author_id=author_id, **validated_data)
        # ModelViewSet handles the response serialization

    def perform_update(self, serializer):
        """Calls the service layer to update a book."""
        validated_data = serializer.validated_data
        author = validated_data.pop('author', None)
        author_id = author.pk if author else None
        instance = self.get_object()
        book_service.update_book(book_id=instance.pk, author_id=author_id, **validated_data)

    def perform_destroy(self, instance):
        """Calls the service layer to delete a book."""
        # Note: This will fail if the book is part of an active transaction
        # due to models.PROTECT in Transaction.book ForeignKey.
        # This is generally desired behavior. Error handling can be added if needed.
        try:
            book_service.delete_book(book_id=instance.pk)
        except Exception as e: # Catch potential ProtectedError
            # Re-raise or handle appropriately
            # For now, let DRF handle it (will likely result in 500 or specific DRF error)
            # A more robust implementation might return a 400 Bad Request with a clear message.
            raise e

    # list/retrieve use the default queryset and serializer, which is fine for now.
    # Override if specific service layer calls are needed (e.g., complex filtering).