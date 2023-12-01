# api_yamdb

Проект YaMDb

### О проекте:
Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Взаимодействие через API.

Доступные endpiont:
```
server/api/v1/signup
server/api/v1/token - получить токен
server/api/v1/auth - авторизоватся
server/api/v1/categories/- список категорий
server/api/v1/genres/ - список жанров
server/api/v1/titles/ - список произведений
server/api/v1/titles/title_id/reviews - отзывы на произведения
server/api/v1/titles/title_id/reviews/review_id/comments - коментарии на отзывы
```


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:TDVwork696/api_yamdb.git
```

```
cd api_yandb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Импортировать данные из csv файлов в базу:

```
python3 manage.py import_csv_to_db
```

Файлы хранятся в директории
```
api_yamdb/static/data/
```
Название файлов:
category.csv - данные категорий
comments.csv - данные коментариев
genre.csv - данные жанров
review.csv - данные отзывов
titles.csv - данные произведений
users.csv - данные пользователей
