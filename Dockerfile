FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Collect static files (if applicable)
# RUN python manage.py collectstatic --noinput

CMD python manage.py runserver 0.0.0.0:8000
