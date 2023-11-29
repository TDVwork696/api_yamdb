from django.core.management.base import BaseCommand

from reviews.models import Categories, Comments, Genres, Review, Title
from user.models import CustomUser

class Command(BaseCommand):
    help = 'Import data from csv to db'

    def handle(self, *args, **options):
        with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = Teacher.objects.get_or_create(
                first_name=row[0],
                last_name=row[1],
                middle_name=row[2],
                )
