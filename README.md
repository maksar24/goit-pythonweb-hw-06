## Налаштування бази даних

Для запуску проєкту потрібна база PostgreSQL.
Команда запуску Docker:
docker run --name hw-postgres-database -p 5432:5432 -e POSTGRES_PASSWORD=maksar24 -d postgres

### Параметри підключення:

Створити свій config.ini з такими даними:
[postgresql]
username = postgres
password = maksar24
domain = localhost
db_name = postgres

### Для зручності додав файл - list_entities.py:

Простий допоміжний скрипт для виведення існуючих записів у базі даних:

- Групи
- Студенти
- Викладачі
- Предмети

Допомагає швидко переглянути реальні назви сутностей у базі даних,
щоб використовувати їх у запитах або тестах.
