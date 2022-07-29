FROM python:3.9-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv lock
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]