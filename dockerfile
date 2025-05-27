# Базовый образ Python
FROM python:3.10-slim

# Установка зависимостей системы (для Postgresql и других библиотек)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/staticfiles && \
    chown -R www-data:www-data /app/staticfiles && \
    chmod -R 755 /app/staticfiles

# Рабочая директория
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Команда для запуска (позже заменим на gunicorn)
CMD ["gunicorn", "The_Best_Diploma_App.wsgi:application", "-b", "0.0.0.0:8000"]