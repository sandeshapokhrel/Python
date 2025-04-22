from django.db import models
from django.contrib.auth.models import User # Import the standard User model

class Student(models.Model):
    """
    Represents a student profile linked to a User account.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, help_text='Unique ID for the student')
    department = models.CharField(max_length=100, null=True, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username # Display the associated username

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"