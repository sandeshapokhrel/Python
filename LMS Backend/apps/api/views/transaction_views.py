from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError # Alias to avoid clash
from apps.core.models import Transaction, Student
from ..serializers.transaction_serializers import TransactionSerializer, BorrowBookSerializer
from apps.services import transaction_service # Import the service functions

# --- Custom Permissions ---
class IsAdminOrTransactionOwner(permissions.BasePermission):
    """
    Custom permission:
    - Allows read access only to admin users or the student who owns the transaction.
    - Write/Delete access typically restricted (handled by borrow/return actions).
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if user is admin or the transaction belongs to the user's student profile
        is_owner = False
        if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
            is_owner = obj.student == request.user.student_profile

        return request.user.is_staff or is_owner

# --- ViewSet ---
class TransactionViewSet(viewsets.ReadOnlyModelViewSet): # Primarily read-only, actions handle changes
    """
    API endpoint for viewing borrowing transactions.
    Provides custom actions for borrowing and returning books.
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTransactionOwner] # Must be logged in, check owner/admin

    def get_queryset(self):
        """
        Filter transactions based on the user.
        Admins see all transactions, students see only their own.
        """
        user = self.request.user
        if user.is_staff:
            return Transaction.objects.select_related('book', 'student__user').all().order_by('-borrow_date')
        elif hasattr(user, 'student_profile'):
            # Ensure student profile exists before filtering
            student_profile = getattr(user, 'student_profile', None)
            if student_profile:
                 return Transaction.objects.filter(student=student_profile).select_related('book', 'student__user').order_by('-borrow_date')
            else:
                 # Should not happen if user is authenticated student, but handle defensively
                 return Transaction.objects.none()
        else:
            # Non-admin, non-student users see nothing
            return Transaction.objects.none()

    # --- Custom Actions ---

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='borrow')
    def borrow_book_action(self, request):
        """
        Custom action for a student to borrow a book.
        Expects {'book_id': <id>} in the request data.
        """
        serializer = BorrowBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']

        try:
            # Ensure the user has a student profile
            if not hasattr(request.user, 'student_profile'):
                return Response({"error": "User does not have an associated student profile."}, status=status.HTTP_400_BAD_REQUEST)

            transaction = transaction_service.borrow_book(user=request.user, book_id=book_id)
            response_serializer = TransactionSerializer(transaction) # Serialize the created transaction
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except (Student.DoesNotExist, Book.DoesNotExist) as e:
             # Should be caught by serializer/permission checks, but handle defensively
             return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except DRFValidationError as e: # Catch validation errors from the service
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log error
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='return')
    def return_book_action(self, request, pk=None):
        """
        Custom action for a student to return a book associated with a specific transaction.
        Uses the transaction ID from the URL (pk).
        """
        transaction_id = pk
        try:
            # Ensure the user has a student profile
            if not hasattr(request.user, 'student_profile'):
                return Response({"error": "User does not have an associated student profile."}, status=status.HTTP_400_BAD_REQUEST)

            transaction = transaction_service.return_book(user=request.user, transaction_id=transaction_id)
            response_serializer = TransactionSerializer(transaction) # Serialize the updated transaction
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
             return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)
        except DRFValidationError as e: # Catch validation errors from the service
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log error
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)