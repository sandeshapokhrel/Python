from rest_framework import serializers
from django.contrib.auth.models import User
from apps.core.models import Student # Import Student model

class StudentRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for student-specific profile data during registration.
    """
    class Meta:
        model = Student
        fields = ['student_id', 'department', 'enrollment_date'] # Fields specific to Student profile
        # 'user' field is handled separately

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, including password confirmation and student profile data.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirm password")
    student_profile = StudentRegistrationSerializer(required=True) # Nested serializer for student data

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'student_profile']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}, # Make email required
        }

    def validate(self, attrs):
        """
        Check that the two password entries match.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # Remove confirmation field after validation
        del attrs['password_confirm']
        return attrs

    def create(self, validated_data):
        """
        Handle creation of User and linked Student profile.
        This method will NOT be called directly. The view will call the service layer.
        We define it here for completeness, but the actual logic resides in the service.
        """
        # This logic should ideally be in the service layer.
        # We raise an error here to enforce using the service.
        raise NotImplementedError("User creation should be handled by the AuthService.")