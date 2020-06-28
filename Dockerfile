FROM python:3.7-alpine

RUN apk add --no-cache postgresql-libs bash && \
	apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

# Adds our application code to the image
COPY . app
WORKDIR app

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 --access-logfile - wsgi:app