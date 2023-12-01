import csv
from django.core.management.base import BaseCommand

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
            # Открываем файл таблицы
            with open(f"../api_yamdb/static/data/{table}.csv") as file:
                # Убираем первую строчку в которой название столбцов
                # (id, name, slug и т.п.)
                heading = next(file).rstrip().split(',')
                reader = csv.reader(file)  # Читаем файл
                model = self.dict[table]  # Получаем модель для таблицы
                for row in reader:
                    objs = {}
                    for i in range(len(heading)):
                        ele = heading[i]  # Получаем название стобца
                        objs[ele] = row[i]
                    # Создаем объект модели
                    model.objects.update_or_create(**objs)
