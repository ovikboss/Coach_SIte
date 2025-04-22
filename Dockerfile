FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем переменные окружения (важно для Django)
ENV DJANGO_SETTINGS_MODULE = coachsite.settings

# Команда для запуска приложения
CMD ["uvicorn", "coachsite.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
