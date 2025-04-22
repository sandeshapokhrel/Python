from rest_framework import serializers
from apps.core.models import Book, Author
from .author_serializers import AuthorSerializer # Import AuthorSerializer for nested representation

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model. Includes nested Author details for reading,
    and accepts author_id for writing/updating.
    """
    # For read operations, show nested author details
    author = AuthorSerializer(read_only=True)
    # For write operations (create/update), accept the author's ID
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'published_date', 'author', 'author_id', 'stock']
        read_only_fields = ['id'] # 'author' is read-only due to definition above

    def validate_isbn(self, value):
        """
        Basic validation for ISBN length (can be enhanced).
        """
        if len(value) != 13 or not value.isdigit():
            # Note: Real ISBN validation is more complex (check digit)
            raise serializers.ValidationError("ISBN must be a 13-digit number.")
        return value

    def validate_stock(self, value):
        """
        Ensure stock is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value