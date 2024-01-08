# Проект «YaMDb»

## О проекте:
Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Взаимодействие через API.

## Инструкция для развёртывания проекта:
### Клонировать репозиторий и перейти в него в командной строке:
`git clone git@github.com:TDVwork696/api_yamdb.git`
`cd api_yandb`

### Cоздать и активировать виртуальное окружение:
`python3 -m venv env`
`source env/bin/activate`
`python3 -m pip install --upgrade pip`

### Установить зависимости из файла requirements.txt:
`python -m pip install --upgrade pip`\
`pip install -r requirements.txt`

### Выполнить миграции:
`python manage.py migrate`

### Запустить проект:
`python manage.py runserver`

### Импортировать данные из csv файлов в базу:
`python3 manage.py import_csv_to_db`

### Файлы хранятся в директории
`api_yamdb/static/data/`

## Название файлов:
category.csv - данные категорий
comments.csv - данные коментариев
genre.csv - данные жанров
review.csv - данные отзывов
titles.csv - данные произведений
users.csv - данные пользователей

## В проекте используются переменные окружения, чтобы использовать их ознакомтесь с файлом:
example.env

## Доступные endpiont:
### - Регистрация нового пользователя:
server/api/v1/auth/signup

### - Получить токен:
server/api/v1/auth/token - получить токен

### - Список категорий:
server/api/v1/categories/

### - Список жанров:
server/api/v1/genres/

###  - Список произведений:
server/api/v1/titles/

### - Отзывы на произведения:
server/api/v1/titles/title_id/reviews

### - Коментарии на отзывы:
server/api/v1/titles/title_id/reviews/review_id/comments 


## Использованные технологии:
- Язык програмирования - Python 3.9.10
- Фреймворк DRF
- СУБД - Sqlite3 

## Об авторах:
https://github.com/TDVwork696
https://github.com/s0branie
https://github.com/svhol