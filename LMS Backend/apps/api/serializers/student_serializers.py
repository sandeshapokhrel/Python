from rest_framework import serializers
from django.contrib.auth.models import User
from apps.core.models import Student

class SimpleUserSerializer(serializers.ModelSerializer):
    """
    A simple serializer for User details, excluding sensitive info like password.
    Used for nested representation within StudentSerializer.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student profile model. Includes nested User details.
    """
    user = SimpleUserSerializer(read_only=True) # Show related user details on read
    # For updates, we might need a separate serializer or handle user_id if needed,
    # but typically student profile updates don't change the linked user.

    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'department', 'enrollment_date']
        read_only_fields = ['id', 'user'] # User link shouldn't be changed via this serializer

    def validate_student_id(self, value):
        """
        Basic validation for student ID format (can be customized).
        """
        # Example: Ensure it's not empty
        if not value:
            raise serializers.ValidationError("Student ID cannot be empty.")
        # Add more specific format checks if needed
        return value