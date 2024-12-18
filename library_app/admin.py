from django.contrib import admin
from .models import Author, Book, BorrowRecord

# Register the Author model
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')  # Fields to display in the list view
    search_fields = ('name',)       # Enable search by name

# Register the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available_copies')
    search_fields = ('title', 'author__name')  # Enable search by title or author's name
    list_filter = ('author',)  # Filter books by author

# Register the BorrowRecord model
@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrowed_by', 'borrow_date', 'return_date')
    search_fields = ('book__title', 'borrowed_by')  # Enable search by book title or borrower name
    list_filter = ('borrow_date', 'return_date')    # Filter by borrow/return date
