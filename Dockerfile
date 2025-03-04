FROM python:3.10

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Установка LibreOffice с явными зависимостями и отладкой
RUN apt-get update && \
    apt-get install -y \
        libreoffice \
        libreoffice-writer \
        libreoffice-java-common \
        default-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    libreoffice --version || echo "LibreOffice installation failed"

# Копируем проект
COPY . /app/

# Открываем порт
EXPOSE 8000

# Запускаем Gunicorn
CMD ["gunicorn", "auto_testing.wsgi:application", "--bind", "0.0.0.0:8000"]