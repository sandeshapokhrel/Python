from rest_framework import serializers
from apps.core.models import Transaction, Book, Student
from .book_serializers import BookSerializer # For nested book details
from .student_serializers import StudentSerializer # For nested student details

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Transaction details.
    Includes nested Book and Student information.
    """
    book = BookSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True) # Include the overdue status

    class Meta:
        model = Transaction
        fields = [
            'id', 'book', 'student', 'borrow_date', 'due_date',
            'return_date', 'status', 'is_overdue'
        ]
        read_only_fields = fields # This serializer is primarily for reading


class BorrowBookSerializer(serializers.Serializer):
    """
    Serializer specifically for the 'borrow book' action.
    Only requires the book_id. The student is inferred from the request user.
    """
    book_id = serializers.IntegerField(required=True, help_text="ID of the book to borrow.")

    def validate_book_id(self, value):
        """Check if the book exists."""
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Book with this ID does not exist.")
        return value

# Note: Returning a book doesn't typically need input data other than the transaction ID
# which is usually part of the URL, so a specific serializer might not be needed,
# or it could be a simple serializer if extra data were required for the return action.