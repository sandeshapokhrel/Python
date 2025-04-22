from django.db import models
from django.utils import timezone
from .book import Book
from .student import Student

class Transaction(models.Model):
    """
    Represents a book borrowing/return transaction.
    """
    STATUS_CHOICES = [
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='transactions') # Protect book from deletion if borrowed
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transactions')
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Borrowed')

    def __str__(self):
        return f"{self.student.user.username} borrowed {self.book.title} on {self.borrow_date.strftime('%Y-%m-%d')}"

    def is_overdue(self):
        """Checks if the book is overdue and not yet returned."""
        return self.status == 'Borrowed' and timezone.now() > self.due_date

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-borrow_date'] # Show most recent transactions first