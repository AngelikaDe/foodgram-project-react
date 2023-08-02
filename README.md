# Foodgram - Продуктовый помощник
Социальная сеть для публикации, обмена рецептами, подписки на авторов. Есть возможность сформировать список покупок для выбранных рецептов.
## Запуск проекта
### Технологии:
` Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL `
### Развернуть проект на удаленном сервере:
* Установить на сервере Docker, Docker Compose
* Скопировать на сервер файлы docker-compose.yml, nginx.conf
* Чтобы запустить проект на серверее:
` sudo docker compose up -d `
* Выполните миграции:
` sudo docker compose exec backend python manage.py migrate ` 
* Соберите статистику:
` sudo docker compose exec backend python manage.py collectstatic --no-input `
* Создайте суперпользователя:
` sudo docker compose exec backend python manage.py createsuperuser `
* Загрузите ингредиенты:
` docker сompose exec backend python manage.py csv_import `