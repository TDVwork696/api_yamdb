import csv
from django.core.management.base import BaseCommand

from reviews.models import Categories, Comments, Genres, Review, Title
from user.models import CustomUser


class Command(BaseCommand):
    """Класс комажны выполняющей импорт данных из файла"""
    help = 'Import data from csv to db'
    path_category = "../api_yamdb/static/data/category.csv"
    path_comments = "../api_yamdb/static/data/comments.csv"
    path_genre = "../api_yamdb/static/data/genre.csv"
    path_genre_title = "../api_yamdb/static/data/genre_title.csv"
    path_review = "../api_yamdb/static/data/review.csv"
    path_titles = "../api_yamdb/static/data/titles.csv"
    path_users = "../api_yamdb/static/data/users.csv"

    def handle(self, *args, **options):

        dict = {
            'category': Categories,
            'genre': Genres
        }

        path_users = "../api_yamdb/static/data/users.csv"

        for table in dict:
            with open(f"../api_yamdb/static/data/{table}.csv") as file:
                    reader = csv.reader(next(file))
                    for row in reader:
                        Comments.objects.get_or_create(
                            id=row[0],
                            review_id=row[1],
                            text=row[2],
                            author_id=row[3],
                            pub_date=row[4]
                        )



"""
    def handle(self, *args, **options):

        with open(self.path_users) as file:
            reader = csv.reader(next(file))
            for row in reader:
                CustomUser.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )

        with open(self.path_category) as file:
            reader = csv.reader(next(file))
            for row in reader:
                Categories.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )

        with open(self.path_genre) as file:
            reader = csv.reader(next(file))
            for row in reader:
                Genres.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )

        with open(self.path_titles) as file:
            reader = csv.reader(next(file))
            for row in reader:
                Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category_id=row[3]
                )

        with open(self.path_review) as file:
            reader = csv.reader(next(file))
            for row in reader:
                Review.objects.get_or_create(
                    id=row[0],
                    title_id=row[1],
                    text=row[2],
                    author_id=row[3],
                    score=row[4],
                    pub_date=row[5]
                )

        with open(self.path_comments) as file:
            reader = csv.reader(next(file))
            for row in reader:
                Comments.objects.get_or_create(
                    id=row[0],
                    review_id=row[1],
                    text=row[2],
                    author_id=row[3],
                    pub_date=row[4]
                )
"""
