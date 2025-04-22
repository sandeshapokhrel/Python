from rest_framework import serializers
from apps.core.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    """
    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date', 'biography']
        # 'id' is included for referencing, usually read-only by default