from django.db import models

class Author(models.Model):
    """
    Model representing an author in the library system.
    """
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model representing a book in the library system.
    """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

class BorrowRecord(models.Model):
    """
    Model representing a book borrowing record.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    borrowed_by = models.CharField(max_length=255)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrowed_by}"