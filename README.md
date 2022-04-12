# Ubuntu 18.04 LTS server настройка
>login: ulugbek
> 
>password: n******9

***

# Установка статичекого ip на Ubuntu 18.4 server
>sudo nano /etc/netplan/00-installer-config.yaml 

```
network:
  version: 2
  ethernets:
    ens33:
       addresses: [192.168.20.160/24]
       gateway4: 192.168.20.2
       nameservers:
         addresses: [192.168.20.2, 8.8.8.8]
```
>sudo netplan apply
****

# PostgreSQL
>db_name: postgres
> 
>db_username: postgresql
> 
> db_password: nc778119
> 
# Разрешить подключение удаленно к PostgreSQL
``` 
sudo nano /etc/postgresql/12/main/postgresql.conf
```

> listen_addresses = '*' 
```
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

```
# IPv4 local connections:
host    all             all             0.0.0.0/0            md5
```

## Открыт порт и перезапустить Postgresql
```
sudo ufw allow 5432/tcp
sudo systemctl restart postgresql
```

***
# 1. Вариант. Настройка Docker (django+gunicorn+nginx)

# Настройка шаблона, замените url сервера показано ниже
> templates/prod_template
``` 
<img src="http://192.168.0.106:1337/static/img/log.png" style="width: 200px"  alt="static/img/agros.png">
<img src="http://192.168.0.106:1337/static/img/sqb.png"  style="width: 120px;text-align: right;float: right"  >
```
## Создайте Dockerfile
``` 
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
```
## Создайте docker-compose.yml
``` 
version: '3.7'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    expose:
      - 8000
    volumes:
      - static_volume:/app/static
    entrypoint:
      - ./entrypoint.sh

  nginx:
    build: ./nginx

    volumes:
      - static_volume:/app/static
    ports:
      - 1337:80
    depends_on:
      - web
volumes:
  static_volume:
```
## Docker команды
```
docker-compose up -d --build
docker-compose down
```
***

## Осторожно! Удаление всех образов! 
``` 
docker rmi $(docker images -q)
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

***
# 2. Вариант. Настройка Django с Postgres, Nginx и Gunicorn в Ubuntu 20.04
> Инструкция: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04-ru
>
Установка пакетов из хранилищ Ubuntu
```
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```
# Создание базы данных и пользователя PostgreSQL
```
sudo -u postgres psql
```
``` 
CREATE DATABASE psb;
CREATE USER agros WITH PASSWORD 'Agr0sugurta.UZ';
```

``` 
ALTER ROLE agros SET client_encoding TO 'utf8';
ALTER ROLE agros SET default_transaction_isolation TO 'read committed';
ALTER ROLE agros SET timezone TO 'UTC';
```
``` 
GRANT ALL PRIVILEGES ON DATABASE psb TO agros;
```
``` 
\q
```
# Создание виртуальной среды Python для проекта PSB
``` 
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
```

```
git clone https://github.com/dohcgle/psb.git
cd psb
```
``` 
virtualenv venv
source venv/bin/activate
```
```
python -m pip install --upgrade pip 
pip3 install -r requirements.txt
```
## Изменение настроек проекта
``` 
sudo nano nano ~/psb/psb/settings.py
```
``` 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'psb',
        'USER': 'agros',
        'PASSWORD': 'Agr0sugurta.UZ',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
# Завершение начальной настройки проекта
``` 
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py collectstatic
```
# Создайте исключение для порта 8000 с помощью следующей команды:
``` 
sudo ufw allow 8000
```
# Запуск сервера
``` 
./manage.py runserver 0.0.0.0:8000
```

# Тестирование способности Gunicorn обслуживать проект
``` 
sudo apt install gunicorn
cd ~/psb
gunicorn --bind 0.0.0.0:8000 psb.wsgi
deactivate
```

# Создание файлов сокета и служебных файлов systemd для Gunicorn
```
sudo nano /etc/systemd/system/gunicorn.socket 
```

``` 
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

``` 
sudo nano /etc/systemd/system/gunicorn.service
```

``` 
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ulugbek
Group=www-data
WorkingDirectory=/home/ulugbek/psb
ExecStart=/home/ulugbek/psb/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          psb.wsgi:application

[Install]
WantedBy=multi-user.target
```

``` 
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
# Проверка файла сокета Gunicorn
``` 
sudo systemctl status gunicorn.socket
```
# Тестирование активации сокета
``` 
sudo systemctl status gunicorn
```
# Перезапуск процесс Gunicorn
``` 
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

# Настройка Nginx как прокси для Gunicorn
``` 
sudo nano /etc/nginx/sites-available/psb
```

``` 
server {
    listen 8000;
    server_name 192.168.2.196, 195.158.9.254;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ulugbek/psb;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
# Сохраните файл и закройте его после завершения. Теперь мы можем активировать файл, привязав его к каталогу
``` 
sudo ln -s /etc/nginx/sites-available/psb /etc/nginx/sites-enabled
```

# Перезапуск Nginx
``` 
sudo systemctl restart nginx
```

# Установка языковой пакет "Число с прописью"

``` 
./static/lang_RU.py нужна скопировать эту файл в каталог venv/lib/num2words
```
## Копирования файла из контейнера
> docker cp psb_web_1:/app/venv/lib/python3.8/site-packages/num2words/lang_TR.py .
> 
> docker cp static/lang_TR.py psb_web_1:/app/venv/lib/python3.8/site-packages/num2words/lang_TR.py
***

***
# Ошибки
> ConnectionRefusedError at /PerformTransactionRequest/
>[Errno 111] Connection refused
## Проверь файл psb/pdf/views.py
> если продакшан тогда: template_path = 'pdf/prod_template.html'
> 
> если в режиме разработки тогда: template_path = 'pdf/customer_template.html'
***
