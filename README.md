# Проект: Веб-приложение для управления задачами

Данный проект представляет собой полноценное веб-приложение для управления задачами, реализованное с использованием Python (FastAPI и Django) для backend'а и React для frontend'а. Приложение поддерживает как асинхронные, так и синхронные API, а также интеграцию с базой данных SQLite. Оно разворачивается в Docker-контейнерах и взаимодействует с фронтендом на React.

## Структура проекта

```
TaskTracker/
├── alembic/               # Директория для миграций базы данных
│   ├── versions/          # Поддиректория с версиями миграций
│   ├── env.py             # Конфигурация Alembic для управления миграциями
│   ├── README             # Описание для Alembic
│   └── script.py.mako     # Шаблон для создания миграций
├── task-manager/          # Папка, предназначенная для управления задачами и фронтенда
│   ├── public/            # Публичные файлы для веб-интерфейса
│   ├── src/               # Исходный код фронтенд части проекта
│   ├── Dockerfile         # Файл Docker для сборки фронтенд-части
│   ├── package-lock.json  # Закрепленные версии зависимостей Node.js
│   ├── package.json       # Описание зависимостей и метаданных для Node.js
│   └── README.md          # Основная документация проекта
├── todo_api_async/        # Асинхронное приложение для работы с задачами
│   └── app/               # Основная директория приложения
│       ├── __init__.py    # Инициализация пакета
│       ├── config.py      # Файл конфигурации для FastAPI
│       ├── crud.py        # CRUD операции для управления задачами
│       ├── database.py    # Управление подключением к базе данных
│       ├── main.py        # Основной файл запуска FastAPI приложения
│       ├── models.py      # Модели данных для SQLAlchemy
│       ├── Pipfile        # Описание зависимостей для использования pipenv
│       └── schemas.py     # Схемы для Pydantic для валидации данных
├── todo_api_sync/         # Синхронное приложение для работы с задачами
│   └── config/            # Папка с конфигурациями
│       ├── __init__.py    # Инициализация пакета
│       ├── asgi.py        # Конфигурация для запуска ASGI сервера
│       ├── settings.py    # Основные настройки проекта
│       ├── urls.py        # Маршрутизация для приложения
│       └── wsgi.py        # Конфигурация для запуска WSGI сервера
├── tasks/                 # Директория для миграций и управления задачами
│   ├── migrations/        # Папка с миграциями базы данных
│   ├── db.sqlite3         # Основная база данных SQLite
│   ├── manage.py          # Скрипт управления Django-приложением
│   └── tests/             # Тесты для приложения
├── .flake8                # Конфигурация для линтера flake8
├── .gitignore             # Игнорируемые файлы и папки для Git
├── alembic.ini            # Конфигурация для Alembic
├── docker-compose.yml     # Файл для управления контейнерами через Docker Compose
├── Dockerfile             # Описание Docker-образа для всего приложения
├── Pipfile                # Описание зависимостей для использования pipenv
├── Pipfile.lock           # Зафиксированные версии зависимостей
└── tasks.db               # База данных для трекинга задач
```


## 1. Запуск приложения

### 1.1. Запуск FastAPI-приложения (асинхронный backend)

Асинхронное приложение реализовано с использованием FastAPI и находится в папке todo_api_async/app.

1. Установите зависимости и выполните миграции::

   ```bash
   pipenv install
   pipenv run alembic upgrade head
   ```

2. Запустите сервер:

    ```bash
    pipenv run uvicorn todo_api_async.app.main:app --reload
    ```
Примечание: Приложение будет доступно по адресу http://127.0.0.1:8000/docs#.

### 1.2. Запуск Django-приложения (синхронный backend)

Синхронное приложение реализовано на Django и находится в папке todo_api_sync.

1. Установите зависимости:

    ```bash
    pipenv install
    ```

2. Выполните миграции:

    ```bash
    pipenv run ./todo_api_sync/manage.py migrate
    ```

3. Запустите сервер:

    ```bash
    pipenv run ./todo_api_sync/manage.py runserver 0.0.0.0:8001
    ```
Примечание: Приложение будет доступно по адресу http://127.0.0.1:8001.

### 1.3. Запуск frontend приложения (React)

Фронтенд-приложение находится в папке task-manager и реализовано на React.

1. Установите зависимости:

    ```bash
    cd task-manager
    npm install
    ```

3. Запустите приложения:

    ```bash
    npm start

    ```
Примечание: React-приложение будет доступно по адресу http://localhost:3000.

## 2. Запуск через Docker

Приложение может быть запущено в контейнере с помощью Docker.

### Шаги для запуска:

1. Соберите Docker-образ:

   ```bash
   docker-compose build
   ```

2. Запустите контейнер через Docker Compose:

    ```bash
    docker-compose up
    ```

После запуска:

FastAPI backend будет доступен по адресу: http://localhost:8000/docs#.
Django backend — http://localhost:8001.
React frontend — http://localhost:3000.

## 3. Эндпоинты FastAPI (асинхронный backend)

 - POST /tasks — Добавление новой задачи.
 - GET /tasks — Получение списка задач с поддержкой фильтрации по статусу и приоритету. Фильтры доступны через query-параметры:

   - completed — статус выполнения задачи (true или false).
   - priority — приоритет задачи (low, medium, high).

    Например, запрос:
    ```bash
    GET http://127.0.0.1:8000/tasks?completed=true&priority=medium
    ```
    Получает список задач со статусом "выполнено" и средним приоритетом.

 - GET /tasks/{task_id} — Получение задачи по её ID.
 - PUT /tasks/{task_id} — Обновление существующей задачи.
 - DELETE /tasks/{task_id} — Удаление задачи.

## 4. Эндпоинты Django (синхронный backend)

 - GET /tasks — Получение списка задач.
 - POST /tasks — Добавление новой задачи.
 - GET /tasks/{task_id}/ — Получение задачи по её ID.
 - PUT /tasks/{task_id}/update — Обновление задачи.
 - DELETE /tasks/{task_id}/delete — Удаление задачи.

## 5. Основные зависимости

 - FastAPI — асинхронный фреймворк для создания API.
 - Django — мощный фреймворк для синхронных веб-приложений.
 - React — фронтенд-библиотека для построения пользовательских интерфейсов.
 - Alembic — инструмент для управления миграциями базы данных.
 - SQLAlchemy — ORM для взаимодействия с базой данных.


## 6. Лицензия

Этот проект лицензирован под лицензией MIT.