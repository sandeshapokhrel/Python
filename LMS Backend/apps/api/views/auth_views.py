from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..serializers.auth_serializers import UserRegistrationSerializer
from apps.services.auth_service import register_user # Import the service function
from django.contrib.auth.models import User

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Accepts POST requests with user and student profile data.
    """
    queryset = User.objects.all() # Required for CreateAPIView, though not directly used for creation here
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # Allow anyone to register

    def create(self, request, *args, **kwargs):
        """
        Handles the POST request for user registration.
        Uses the service layer function for actual user creation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # Validate input data

        try:
            # Call the service function to handle user and student creation
            user = register_user(serializer.validated_data)
            # Optionally return some user data upon successful registration
            # For security, avoid returning the password.
            # We can create another simple serializer for the response if needed.
            response_data = {
                "message": "User registered successfully.",
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Catch potential errors from the service layer (like validation errors)
            # The service layer raises serializers.ValidationError for specific cases
            # Other exceptions are caught here as a fallback
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)