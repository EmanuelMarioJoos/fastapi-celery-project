FROM python:3.9-buster

WORKDIR /code

ADD . /app/
WORKDIR /app/
RUN pip install -r requirements.txt

CMD ["echo", "hello"]