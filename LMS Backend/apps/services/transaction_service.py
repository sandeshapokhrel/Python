from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from apps.core.models import Book, Student, Transaction
from rest_framework.exceptions import ValidationError # Use DRF's validation error for API consistency
from typing import List

# Define borrowing period (e.g., 14 days)
BORROWING_PERIOD_DAYS = 14

@transaction.atomic # Ensure book stock and transaction are updated together
def borrow_book(user: User, book_id: int) -> Transaction:
    """
    Handles the process of a student borrowing a book.

    Args:
        user (User): The user (student) borrowing the book.
        book_id (int): The ID of the book to borrow.

    Returns:
        Transaction: The newly created transaction record.

    Raises:
        Student.DoesNotExist: If the user does not have a student profile.
        Book.DoesNotExist: If the book_id is invalid.
        ValidationError: If the book is out of stock or other business rule violations.
    """
    student = get_object_or_404(Student, user=user)
    book = get_object_or_404(Book, pk=book_id)

    # Check if the book is in stock
    if book.stock <= 0:
        raise ValidationError(f"'{book.title}' is currently out of stock.")

    # Optional: Check if the student already has this book borrowed and not returned
    existing_borrow = Transaction.objects.filter(
        student=student,
        book=book,
        status='Borrowed'
    ).exists()
    if existing_borrow:
        raise ValidationError(f"You have already borrowed '{book.title}' and not returned it yet.")

    # Decrement stock and create transaction
    book.stock -= 1
    book.save()

    due_date = timezone.now() + timedelta(days=BORROWING_PERIOD_DAYS)
    new_transaction = Transaction.objects.create(
        book=book,
        student=student,
        due_date=due_date,
        status='Borrowed'
        # borrow_date is set automatically by default=timezone.now
    )
    return new_transaction

@transaction.atomic
def return_book(user: User, transaction_id: int) -> Transaction:
    """
    Handles the process of a student returning a book.

    Args:
        user (User): The user (student) returning the book.
        transaction_id (int): The ID of the borrowing transaction.

    Returns:
        Transaction: The updated transaction record.

    Raises:
        Student.DoesNotExist: If the user does not have a student profile.
        Transaction.DoesNotExist: If the transaction_id is invalid.
        ValidationError: If the transaction doesn't belong to the user or is already returned.
    """
    student = get_object_or_404(Student, user=user)
    transaction_obj = get_object_or_404(
        Transaction.objects.select_related('book'), # Optimize book fetching
        pk=transaction_id
    )

    # Verify the transaction belongs to the student and is currently borrowed
    if transaction_obj.student != student:
        raise ValidationError("This transaction does not belong to you.")
    if transaction_obj.status != 'Borrowed':
        raise ValidationError(f"This book ('{transaction_obj.book.title}') was already returned or the transaction status is invalid.")

    # Increment stock and update transaction
    book = transaction_obj.book
    book.stock += 1
    book.save()

    transaction_obj.status = 'Returned'
    transaction_obj.return_date = timezone.now()
    transaction_obj.save()

    return transaction_obj

def list_transactions_for_student(user: User) -> List[Transaction]:
    """Returns a list of all transactions for a given student (user)."""
    student = get_object_or_404(Student, user=user)
    return Transaction.objects.filter(student=student).select_related('book').order_by('-borrow_date')

def get_transaction_by_id(transaction_id: int) -> Transaction:
    """Retrieves a single transaction by its ID."""
    return get_object_or_404(Transaction.objects.select_related('book', 'student__user'), pk=transaction_id)