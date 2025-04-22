from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from apps.core.models import Student
from typing import List, Optional

def list_students() -> List[Student]:
    """Returns a list of all students with their related user info."""
    # Use select_related to optimize fetching the related user
    return Student.objects.select_related('user').all()

def get_student_by_id(student_pk: int) -> Student:
    """
    Retrieves a single student profile by its primary key (ID).
    Raises Http404 if not found.
    """
    # Use select_related to optimize fetching the related user
    return get_object_or_404(Student.objects.select_related('user'), pk=student_pk)

def get_student_by_user(user: User) -> Student:
    """
    Retrieves a student profile associated with a given User object.
    Raises Http404 if not found.
    """
    return get_object_or_404(Student.objects.select_related('user'), user=user)

def update_student_profile(student_pk: int, student_id: str, department: Optional[str] = None, enrollment_date: Optional[str] = None) -> Student:
    """
    Updates an existing student profile.
    Note: Does not update the associated User object (username, email etc.).

    Args:
        student_pk (int): The primary key of the Student profile to update.
        student_id (str): The updated unique student ID.
        department (Optional[str]): The updated department.
        enrollment_date (Optional[str]): The updated enrollment date (YYYY-MM-DD).

    Returns:
        Student: The updated student profile object.

    Raises:
        IntegrityError: If the updated student_id conflicts with another student.
    """
    student = get_student_by_id(student_pk)
    student.student_id = student_id
    student.department = department
    student.enrollment_date = enrollment_date
    student.save()
    return student

def delete_student(student_pk: int) -> None:
    """
    Deletes a student profile by its primary key.
    WARNING: This also deletes the associated User account due to on_delete=models.CASCADE.
             Consider if this is the desired behavior. Maybe deactivate the user instead?
             For now, implementing as delete based on the cascade setting.
    """
    student = get_student_by_id(student_pk)
    # Deleting the Student object will cascade and delete the associated User.
    student.delete()

# Note: Student creation is handled in auth_service.register_user