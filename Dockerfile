FROM python:3.8-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN mkdir -p /app/netguru_recruitment_task/static
RUN python manage.py collectstatic --noinput

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN chmod a+rw /app/
RUN chmod 777 /app/db.sqlite3

# add and run as non-root user
RUN adduser -D myuser

USER myuser

# run gunicorn
CMD gunicorn netguru_recruitment_task.wsgi:application --bind 0.0.0.0:$PORT