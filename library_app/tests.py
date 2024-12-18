from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book, BorrowRecord

class AuthorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author_data = {
            'name': 'Test Author',
            'bio': 'A test author biography'
        }
        self.author = Author.objects.create(**self.author_data)

    def test_create_author(self):
        """
        Test creating a new author
        """
        response = self.client.post(reverse('author-list'), self.author_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_retrieve_author(self):
        """
        Test retrieving a specific author
        """
        response = self.client.get(reverse('author-detail', kwargs={'pk': self.author.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author_data['name'])

class BookBorrowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            isbn='1234567890123',
            available_copies=5
        )

    def test_borrow_book(self):
        """
        Test borrowing a book
        """
        borrow_data = {
            'book': self.book.id,
            'borrowed_by': 'John Doe'
        }
        response = self.client.post(reverse('borrow-borrow'), borrow_data)
        
        # Refresh book from database
        self.book.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.book.available_copies, 4)
        self.assertEqual(BorrowRecord.objects.count(), 1)

    def test_return_book(self):
        """
        Test returning a borrowed book
        """
        # First, borrow the book
        borrow_record = BorrowRecord.objects.create(
            book=self.book, 
            borrowed_by='John Doe'
        )
        self.book.available_copies -= 1
        self.book.save()

        # Then return the book
        response = self.client.put(
            reverse('borrow-return-book', kwargs={'pk': borrow_record.id})
        )
        
        # Refresh book from database
        self.book.refresh_from_db()
        borrow_record.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book.available_copies, 1)
        self.assertIsNotNone(borrow_record.return_date)