  GNU nano 6.2                           Dockerfile                                     
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "auto_testing.wsgi:application", "--bind", "0.0.0.0:8000"]
