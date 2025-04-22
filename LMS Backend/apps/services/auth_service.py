from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from apps.core.models import Student
from rest_framework import serializers # For validation errors

@transaction.atomic # Ensure User and Student are created together or not at all
def register_user(validated_data):
    """
    Creates a new User and their associated Student profile.

    Args:
        validated_data (dict): Data validated by UserRegistrationSerializer.

    Returns:
        User: The newly created user object.

    Raises:
        serializers.ValidationError: If username or student_id already exists.
        Exception: For other potential errors during creation.
    """
    student_profile_data = validated_data.pop('student_profile')
    password = validated_data.pop('password') # Handled by create_user

    try:
        # Create the User instance (handles password hashing)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'), # Use .get() for optional fields
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # Create the linked Student profile
        Student.objects.create(
            user=user,
            student_id=student_profile_data['student_id'],
            department=student_profile_data.get('department'),
            enrollment_date=student_profile_data.get('enrollment_date')
        )

        return user

    except IntegrityError as e:
        # Handle potential unique constraint violations (e.g., username, student_id)
        # This provides more specific feedback than a generic 500 error.
        if 'auth_user_username_key' in str(e) or 'UNIQUE constraint failed: auth_user.username' in str(e):
             raise serializers.ValidationError({'username': ['A user with that username already exists.']})
        elif 'core_student_student_id_key' in str(e) or 'UNIQUE constraint failed: core_student.student_id' in str(e):
             raise serializers.ValidationError({'student_profile': {'student_id': ['A student with that ID already exists.']}})
        else:
            # Re-raise other integrity errors
            raise e
    except Exception as e:
        # Log the exception here in a real application
        # logger.error(f"Error during user registration: {e}")
        raise Exception(f"An unexpected error occurred during registration: {e}")