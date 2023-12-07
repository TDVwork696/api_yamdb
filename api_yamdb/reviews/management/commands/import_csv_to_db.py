import csv
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Categories, Comments, Genres, Review, Title
from user.models import CustomUser


class Command(BaseCommand):
    help = 'Import data from csv to db'

    dict = {
        'users': CustomUser,
        'genre': Genres,
        'category': Categories,
        'titles': Title,
        'review': Review,
        'comments': Comments,
    }

    def handle(self, *args, **options):
        for table in self.dict:
            try:
                with open(f"../api_yamdb/static/data/{table}.csv") as file:
                    # Убираем первую строчку в которой название столбцов
                    # (id, name, slug и т.п.)
                    heading = next(file).rstrip().split(',')
                    reader = csv.reader(file)
                    model = self.dict[table]  # Получаем модель для таблицы
                    spisok = []
                    for row in reader:
                        objs = {}
                        for i in range(len(heading)):
                            objs[heading[i]] = row[i]
                        spisok.append(model(**objs))
                    model.objects.bulk_create(spisok)
            except FileNotFoundError:
                raise CommandError(f'File not found: {table}')
            except Exception as e:
                raise CommandError(f'Error processing file: {str(e)}')
