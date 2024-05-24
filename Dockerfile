FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /catalog-service

COPY ./requirements.txt /catalog-service/requirements.txt

RUN apt-get update

RUN apt-get install gcc default-libmysqlclient-dev -y

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /catalog-service/src

COPY .env /catalog-service/.env

WORKDIR /catalog-service/src

CMD ["python", "manage.py", "runserver"]

