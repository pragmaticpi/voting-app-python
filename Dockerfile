FROM python:3.6-alpine
LABEL Name=voting-app-python Version=0.0.1

RUN apk update && apk add gcc && apk add libc-dev

COPY . /app
WORKDIR /app

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]
