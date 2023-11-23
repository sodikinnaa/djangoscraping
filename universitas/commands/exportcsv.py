# your_app/management/commands/exportcsv.py
import csv
from django.http import HttpResponse
from django.core.management.base import BaseCommand
from django.utils import timezone
from .models import Detail_cited  # Ganti 'YourModel' dengan nama sebenarnya model Anda

class Command(BaseCommand):
    help = 'Ekspor data ke CSV'

    def handle(self, *args, **options):
        # Tentukan field model yang ingin diekspor
        fields = ['nama_dosen', 'email', 'cited_by']  # Ganti dengan nama field yang sesuai

        # Ambil data dari model
        queryset = Detail_cited.objects.all()  # Ganti 'YourModel' dengan nama sebenarnya model Anda

        # Buat response CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="exported_data_{timezone.now()}.csv"'

        # Buat writer CSV dan tulis header
        csv_writer = csv.writer(response)
        csv_writer.writerow(fields)

        # Tulis baris data
        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in fields])

        self.stdout.write(self.style.SUCCESS('Data diekspor'))

        return response
