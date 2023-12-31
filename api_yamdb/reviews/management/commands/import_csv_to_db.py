import csv
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Categories, Comments, Genres, Review, Title
from user.models import CustomUser


class ImportUser:

    def __init__(self):
        self.file = open("../api_yamdb/static/data/users.csv", mode='r')

    def import_data(self):
        with self.file:
            next(self.file).rstrip().split(',')
            reader = csv.reader(self.file)
            spisok = []
            for row in reader:
                id, username, email, role, bio, first_name, last_name = row
                spisok.append(CustomUser(
                    id=id,
                    username=username,
                    email=email,
                    role=role,
                    bio=bio,
                    first_name=first_name,
                    last_name=last_name))
            CustomUser.objects.bulk_create(spisok)


class ImportGenre:

    def __init__(self):
        self.file = open("../api_yamdb/static/data/genre.csv", mode='r')

    def import_data(self):
        with self.file:
            next(self.file).rstrip().split(',')
            reader = csv.reader(self.file)
            spisok = []
            for row in reader:
                id, name, slug = row
                spisok.append(Genres(id=id,
                                     name=name,
                                     slug=slug))
            Genres.objects.bulk_create(spisok)


class ImportCategory:

    def __init__(self):
        self.file = open("../api_yamdb/static/data/category.csv", mode='r')

    def import_data(self):
        with self.file:
            next(self.file).rstrip().split(',')
            reader = csv.reader(self.file)
            spisok = []
            for row in reader:
                id, name, slug = row
                spisok.append(Categories(id=id,
                                         name=name,
                                         slug=slug))
            Categories.objects.bulk_create(spisok)


class ImportTitle:

    def __init__(self):
        self.file = open("../api_yamdb/static/data/titles.csv", mode='r')

    def import_data(self):
        with self.file:
            next(self.file).rstrip().split(',')
            reader = csv.reader(self.file)
            spisok = []
            for row in reader:
                id, name, year, category_id = row
                spisok.append(Title(id=id,
                                    name=name,
                                    year=year,
                                    category_id=category_id))
            Title.objects.bulk_create(spisok)


class ImportReview:

    def __init__(self):
        self.file = open("../api_yamdb/static/data/review.csv", mode='r')

    def import_data(self):
        with self.file:
            next(self.file).rstrip().split(',')
            reader = csv.reader(self.file)
            spisok = []
            for row in reader:
                id, title_id, text, author_id, score, pub_date = row
                spisok.append(Review(id=id,
                                     title_id=title_id,
                                     text=text,
                                     author_id=author_id,
                                     score=score,
                                     pub_date=pub_date))
            Review.objects.bulk_create(spisok)


class ImportComments:

    def __init__(self):
        self.file = open("../api_yamdb/static/data/comments.csv", mode='r')

    def import_data(self):
        with self.file:
            next(self.file).rstrip().split(',')
            reader = csv.reader(self.file)
            spisok = []
            for row in reader:
                id, review_id, text, author_id, pub_date = row
                spisok.append(Comments(id=id,
                                       review_id=review_id,
                                       text=text,
                                       author_id=author_id,
                                       pub_date=pub_date))
            Comments.objects.bulk_create(spisok)


TABLE_FOR_IMPORT = {
    'user': ImportUser,
    'genre': ImportGenre,
    'category': ImportCategory,
    'title': ImportTitle,
    'review': ImportReview,
    'comments': ImportComments
}


class Command(BaseCommand):
    help = 'Import data from csv to db'

    def handle(self, *args, **options):
        try:
            for import_table in TABLE_FOR_IMPORT:
                class_import = TABLE_FOR_IMPORT[import_table]()
                class_import.import_data()

        except FileNotFoundError:
            raise CommandError(f'File not found {import_table}')
        except Exception as e:
            raise CommandError(f'Error processing file: {str(e)}')
