FROM python:3.9-alpine

# set environment variables
ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

RUN apk --update add
RUN apk add gcc libc-dev libffi-dev jpeg-dev zlib-dev libjpeg
RUN apk add postgresql-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./entrypoint.sh .



RUN chmod +x entrypoint.sh
RUN pip install -r requirements.txt


# copy project
COPY . .
ENTRYPOINT ["/app/entrypoint.sh"]