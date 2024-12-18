from rest_framework import serializers
from .models import Author, Book, BorrowRecord

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    """
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    """
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'isbn', 'available_copies']

class BorrowRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the BorrowRecord model.
    """
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'book_title', 'borrowed_by', 'borrow_date', 'return_date']