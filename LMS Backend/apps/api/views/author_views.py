from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly # Use default from settings
from apps.core.models import Author
from ..serializers.author_serializers import AuthorSerializer
from apps.services import author_service # Import the service functions

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    Uses the AuthorService for business logic.
    """
    queryset = Author.objects.all().order_by('name') # Base queryset
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Default permission

    # Override standard methods to use the service layer

    def perform_create(self, serializer):
        """Calls the service layer to create an author."""
        # Serializer validation happens before this method is called
        validated_data = serializer.validated_data
        author_service.create_author(**validated_data)
        # Note: ModelViewSet's default response handling works fine here,
        # it will return the serialized data of the created object implicitly.
        # If custom response is needed, override create() method fully.

    def perform_update(self, serializer):
        """Calls the service layer to update an author."""
        validated_data = serializer.validated_data
        instance = self.get_object() # Get the instance being updated
        author_service.update_author(author_id=instance.pk, **validated_data)

    def perform_destroy(self, instance):
        """Calls the service layer to delete an author."""
        author_service.delete_author(author_id=instance.pk)

    # Optional: Override list/retrieve if custom logic/serialization is needed
    # def list(self, request, *args, **kwargs):
    #     queryset = author_service.list_authors()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = author_service.get_author_by_id(kwargs['pk'])
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)