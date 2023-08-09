# Foodgram - Продуктовый помощник
## ip: 158.160.31.32 
## доменное имя: yafoodgram.hopto.org
## логин суперюзера: root@yandex.ru, пароль: 0000
Социальная сеть для публикации, обмена рецептами, подписки на авторов. Есть возможность сформировать список покупок для выбранных рецептов.
## Запуск проекта
### Технологии:
` Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL `
### Развернуть проект на удаленном сервере:
* Установить на сервере Docker, Docker Compose
* Скопировать на сервер файлы docker-compose.yml, nginx.conf
* Создать .env файл на сервере
  Например:
```
  DB_ENGINE               # django.db.backends.postgresql
  DB_NAME                 # postgres
  POSTGRES_USER           # postgres
  POSTGRES_PASSWORD       # postgres
  DB_HOST                 # db
  DB_PORT                 # 5432 (порт по умолчанию)
```
* Чтобы запустить проект на серверее:
` sudo docker compose up -d `
* Выполните миграции:
` sudo docker compose exec backend python manage.py makemigrations `
` sudo docker compose exec backend python manage.py migrate `
* Соберите статистику:
` sudo docker compose exec backend python manage.py collectstatic --no-input `
* Создайте суперпользователя:
` sudo docker compose exec backend python manage.py createsuperuser `
* Загрузите ингредиенты:
` docker сompose exec backend python manage.py csv_import `

## Развернуть бэк проекта на локальной машине:
* Склонировать репозиторий
* Создать и активировать venv
` python -m venv venv`
` source venv/bin/activate`
* Установить все завсисимости
`pip install -r requirements`
* Сделать миграции
`python manage.py makemigrations`
`python manage.py migrate`
* Запустить сервер
`python manage.py runserver`
* Можно делать запросы через постман
  #### Примеры:
  Регистрация пользователя:
  POST http://localhost/api/users/
```
  {
      "email": "newuser@yandex.ru",
      "username": "User1",
      "first_name": "Кирилл",
      "last_name": "Иванов",
      "password": "erutnfhv3455"
  }
```
  Получение токена:
POST http://localhost/api/auth/token/login/
```
   {
      "password": "Qwerty777",
      "email": "abcde@yandex.ru"
   }
 ```
  Авторизация:
  POST http://localhost/api/auth/token/login/
```
   {
      "email": "newuser@yandex.ru",
      "password": "erutnfhv3455"
  }
```
Создание рецепта:
http://localhost/api/recipes
```
  {
    "ingredients": [
      {
        "id": 1,
        "amount": 10
      }
    ],
    "tags": [
      1
     ]
    "image": "data:image",
    "name": "string",
    "text": "string",
    "cooking_time": 10
  } 
```

### Автор:
api, деплой - Анжелика Демина
