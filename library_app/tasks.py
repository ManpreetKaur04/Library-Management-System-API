import os
import json
import logging
from datetime import datetime
from django.conf import settings
from celery import shared_task
from .models import Author, Book, BorrowRecord

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def generate_library_report(self):
    """
    Celery task to generate a library activity report.
    """
    try:
        # Create reports directory in the project root
        reports_dir = os.path.join(settings.BASE_DIR, 'reports')
        os.makedirs(reports_dir, exist_ok=True)

        # Generate report data
        report_data = {
            'total_authors': Author.objects.count(),
            'total_books': Book.objects.count(),
            'total_books_borrowed': BorrowRecord.objects.filter(return_date__isnull=True).count(),
            'timestamp': datetime.now().isoformat()
        }

        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'report_{timestamp}.json'
        filepath = os.path.join(reports_dir, filename)

        # Save report to JSON file
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=4)

        logger.info(f"Library report generated: {reports_dir}")
        return {
            'status': 'success',
            'filepath': filepath,
            'data': report_data
        }
    
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }