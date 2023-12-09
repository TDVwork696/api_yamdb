import csv
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Categories, Comments, Genres, Review, Title
from user.models import CustomUser


class Command(BaseCommand):
    help = 'Import data from csv to db'

    def import_user(self):
        with open("../api_yamdb/static/data/users.csv", mode='r') as file:
            heading = next(file).rstrip().split(',')
            reader = csv.reader(file)
            spisok = (CustomUser(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]) for row in reader
            )
            CustomUser.objects.bulk_create(spisok)

    def import_genre(self):
        with open("../api_yamdb/static/data/genre.csv", mode='r') as file:
            heading = next(file).rstrip().split(',')
            reader = csv.reader(file)
            spisok = (Genres(
                id=row[0],
                name=row[1],
                slug=row[2]
            ) for row in reader
            )
            Genres.objects.bulk_create(spisok)

    def import_category(self):
        with open("../api_yamdb/static/data/category.csv", mode='r') as file:
            heading = next(file).rstrip().split(',')
            reader = csv.reader(file)
            spisok = (Categories(
                id=row[0],
                name=row[1],
                slug=row[2]
            ) for row in reader
            )
            Categories.objects.bulk_create(spisok)

    def import_titles(self):
        with open("../api_yamdb/static/data/titles.csv", mode='r') as file:
            heading = next(file).rstrip().split(',')
            reader = csv.reader(file)
            spisok = (Title(
                id=row[0],
                name=row[1],
                year=row[2],
                category_id=row[3]
            ) for row in reader
            )
            Title.objects.bulk_create(spisok)

    def import_review(self):
        with open("../api_yamdb/static/data/review.csv", mode='r') as file:
            heading = next(file).rstrip().split(',')
            reader = csv.reader(file)
            spisok = (Review(
                id=row[0],
                title_id=row[1],
                text=row[2],
                author_id=row[3],
                score=row[4],
                pub_date=row[5]
            ) for row in reader
            )
            Review.objects.bulk_create(spisok)

    def import_comments(self):
        with open("../api_yamdb/static/data/comments.csv") as file:
            heading = next(file).rstrip().split(',')
            reader = csv.reader(file)
            spisok = (Comments(
                id=row[0],
                review_id=row[1],
                text=row[2],
                author_id=row[3],
                pub_date=row[4]
            ) for row in reader
            )
            Comments.objects.bulk_create(spisok)

    def handle(self, *args, **options):
        try:
            self.import_user()
            self.import_genre()
            self.import_category()
            self.import_titles()
            self.import_review()
            self.import_comments()

        except FileNotFoundError:
            raise CommandError('File not found')
        except Exception as e:
            raise CommandError(f'Error processing file: {str(e)}')
