import os
import json
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from library_project import settings

from .models import Author, Book, BorrowRecord
from .serializers import AuthorSerializer, BookSerializer, BorrowRecordSerializer
from .tasks import generate_library_report

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Author model operations with JWT authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model operations with JWT authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BorrowRecord model operations with JWT authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    @action(detail=False, methods=['POST'])
    def borrow(self, request):
        """
        Endpoint to borrow a book.
        Reduces available copies and creates a borrow record.
        """
        book_id = request.data.get('book')
        borrowed_by = request.user.username  # Use authenticated user's username

        try:
            book = Book.objects.get(id=book_id)
            
            if book.available_copies <= 0:
                return Response(
                    {'error': 'No available copies of this book.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Reduce available copies
            book.available_copies -= 1
            book.save()

            # Create borrow record
            borrow_record = BorrowRecord.objects.create(
                book=book,
                borrowed_by=borrowed_by
            )

            return Response(
                BorrowRecordSerializer(borrow_record).data,
                status=status.HTTP_201_CREATED
            )

        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['PUT'])
    def return_book(self, request, pk=None):
        """
        Endpoint to return a borrowed book.
        Increases available copies and updates return date.
        """
        try:
            borrow_record = BorrowRecord.objects.get(
                id=pk, 
                borrowed_by=request.user.username,  # Ensure user can only return their own books
                return_date__isnull=True
            )
            book = borrow_record.book

            # Increase available copies
            book.available_copies += 1
            book.save()

            # Update return date
            borrow_record.return_date = datetime.now().date()
            borrow_record.save()

            return Response(
                BorrowRecordSerializer(borrow_record).data,
                status=status.HTTP_200_OK
            )

        except BorrowRecord.DoesNotExist:
            return Response(
                {'error': 'Borrow record not found or already returned.'},
                status=status.HTTP_404_NOT_FOUND
            )

class ReportViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def retrieve_latest_report(self, request):
        """
        Retrieve the latest generated report.
        """
        reports_dir = os.path.join(settings.BASE_DIR, 'reports')
        
        if not os.path.exists(reports_dir):
            return Response(
                {'error': 'No reports have been generated yet.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get the latest report file
        report_files = [f for f in os.listdir(reports_dir) if f.startswith('report_') and f.endswith('.json')]
        
        if not report_files:
            return Response(
                {'error': 'No reports found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        latest_report_file = max(report_files)
        
        try:
            with open(os.path.join(reports_dir, latest_report_file), 'r') as f:
                report_data = json.load(f)
            return Response(report_data)
        except Exception as e:
            return Response(
                {'error': f'Error reading report: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['POST'])
    def generate_report(self, request):
        """
        Trigger report generation using Celery.
        """
        try:
            # Trigger Celery task
            task = generate_library_report.delay()
            
            return Response({
                'message': 'Report generation started.',
                'task_id': str(task.id)  # Convert UUID to string
            }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({
                'error': f'Error starting report generation: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)