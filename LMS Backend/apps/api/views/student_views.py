from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from apps.core.models import Student
from ..serializers.student_serializers import StudentSerializer
from apps.services import student_service # Import the service functions

# --- Custom Permissions ---
class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Allows read access to any authenticated user.
    - Allows write access only to admin users or the student themselves.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions are only allowed to the owner of the profile or admin users.
        return obj.user == request.user or request.user.is_staff


# --- ViewSet ---
class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing Student profiles.
    Creation is handled via user registration endpoint.
    Deletion might be restricted or handled differently (e.g., deactivation).
    """
    queryset = Student.objects.select_related('user').all().order_by('user__username')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwnerOrReadOnly] # Must be logged in, then check admin/owner

    # Disable POST (creation) via this endpoint - use registration
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']

    def perform_update(self, serializer):
        """Calls the service layer to update a student profile."""
        # Permission check (IsAdminOrOwnerOrReadOnly) happens before this
        validated_data = serializer.validated_data
        instance = self.get_object()
        student_service.update_student_profile(student_pk=instance.pk, **validated_data)

    def perform_destroy(self, instance):
        """
        Handles deletion. Default is CASCADE delete of User.
        Admins can delete any profile. Students might only delete their own (if allowed).
        """
        # Permission check (IsAdminOrOwnerOrReadOnly) ensures only owner or admin can delete
        # Consider adding a confirmation step or soft delete/deactivation instead.
        if not (instance.user == self.request.user or self.request.user.is_staff):
             raise PermissionDenied("You do not have permission to delete this profile.")

        student_service.delete_student(student_pk=instance.pk)

    # list/retrieve use default implementation with permission checks.