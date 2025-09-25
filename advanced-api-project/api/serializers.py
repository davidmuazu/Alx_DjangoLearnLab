from rest_framework import serializers
from .models import Author, Book
import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    Includes validation to prevent future publication years.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    Includes a nested BookSerializer to display related books.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
