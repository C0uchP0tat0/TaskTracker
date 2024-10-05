# Указываем базовый образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем необходимые файлы
COPY Pipfile Pipfile.lock alembic.ini ./

# Устанавливаем pipenv и зависимости
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --ignore-pipfile

# Копируем код приложения FastAPI
COPY ./todo_api_async ./todo_api_async
# Копируем папку с миграциями
COPY ./alembic ./alembic
# Копируем код приложения Django
COPY ./todo_api_sync ./todo_api_sync
# # Копируем код приложения React
# COPY ./task-manager ./task-manager
