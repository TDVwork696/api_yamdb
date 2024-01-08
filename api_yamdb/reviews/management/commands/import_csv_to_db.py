import contextlib
import csv
from os import path

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Categories, Comments, Genres, Review, Title
from user.models import CustomUser

PATH = "../api_yamdb/static/data/"


class Import:

    model = None

    def __init__(self, name_file):
        self.file = path.join(PATH + name_file)
        self.list_models_instances = []

    def create_list(self, row):
        raise NotImplementedError(
            'Нужно реализовать этот метод в подклассах'
        )

    def import_data(self):
        with self.open_file() as file:
            next(file).rstrip().split(',')
            reader = csv.reader(file)
            for row in reader:
                self.create_list(row)
            self.model.objects.bulk_create(self.list_models_instances)

    @contextlib.contextmanager
    def open_file(self):
        self.file = open(self.file, mode='r')
        try:
            yield self.file
        finally:
            self.file.close()


class ImportUser(Import):

    model = CustomUser

    def create_list(self, row):
        id, username, email, role, bio, first_name, last_name = row
        self.list_models_instances.append(self.model(
            id=id,
            username=username,
            email=email,
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name)
        )


class ImportGenre(Import):

    model = Genres

    def create_list(self, row):
        id, name, slug = row
        self.list_models_instances.append(self.model(
            id=id,
            name=name,
            slug=slug)
        )


class ImportCategory(Import):

    model = Categories

    def create_list(self, row):
        id, name, slug = row
        self.list_models_instances.append(self.model(
            id=id,
            name=name,
            slug=slug)
        )


class ImportTitle(Import):

    model = Title

    def create_list(self, row):
        id, name, year, category_id = row
        self.list_models_instances.append(self.model(
            id=id,
            name=name,
            year=year,
            category_id=category_id)
        )


class ImportReview(Import):

    model = Review

    def create_list(self, row):
        id, title_id, text, author_id, score, pub_date = row
        self.list_models_instances.append(self.model(
            id=id,
            title_id=title_id,
            text=text,
            author_id=author_id,
            score=score,
            pub_date=pub_date)
        )


class ImportComments(Import):

    model = Comments

    def create_list(self, row):
        id, review_id, text, author_id, pub_date = row
        self.list_models_instances.append(self.model(
            id=id,
            review_id=review_id,
            text=text,
            author_id=author_id,
            pub_date=pub_date)
        )


TABLE_FOR_IMPORT = {
    ImportUser: 'users.csv',
    ImportGenre: 'genre.csv',
    ImportCategory: 'category.csv',
    ImportTitle: 'titles.csv',
    ImportReview: 'review.csv',
    ImportComments: 'comments.csv'
}


class Command(BaseCommand):
    help = 'Import data from csv to db'

    def handle(self, *args, **options):
        try:
            for import_class, import_file in TABLE_FOR_IMPORT.items():
                import_class(import_file).import_data()

        except FileNotFoundError:
            raise CommandError(f'File not found {import_file}')
        except Exception as e:
            raise CommandError(f'Error processing file: {str(e)}')
