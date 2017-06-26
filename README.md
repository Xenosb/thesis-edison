# Smartbed Edison



## Requirements

To get the project up and running, you will need to install some basic prerequisites. Depending if you are developing just the web part on client machine or testing integration on Edison, you will have to configure the system differently. 

On fedora
```sh
sudo dnf install python python-pip python-devel nginx postgresql gcc
sudo pip install uwsgi flask psycopg2 flask_migrate flask_script flask_sqlalchemy
```

On ubuntu/debian
```sh
sudo apt update
sudo apt install
sudo pip install uwsgi flask psycopg2 flask_migrate flask_script flask_sqlalchemy
```

## Setup

```/etc/systemd/system/smartbed.service```
```sh
[Unit]
Description=Smartbed uWSGI Service

[Service]
Environment="SMARTBED_DIR=/var/www/thesis-edison"
ExecStartPre=/usr/bin/bash -c 'mkdir -p /run/uwsgi; chown <user>:nginx /run/uwsgi'
ExecStart=/usr/bin/bash -c 'cd $SMARTBED_DIR/app; uwsgi --ini $SMARTBED_DIR/app/smartbed.ini;'

[Install]
WantedBy=multi-user.target
```

```sh
mkdir -p /var/sites/smartbed/logs
mkdir -p /run/uwsgi
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled
```

Open */etc/nginx/nginx.conf* and comment out ```server{ ... }``` block and add to the end of the file
```
include /etc/nginx/sites-enabled/*.conf;
server_names_hash_bucket_size 64;
```

Take care to replace *<SMARTBED_DIR>* with absolute path to directory.
Also, make sure that all directories in the path have execute permission.

```/etc/nginx/sites-available/smartbed.conf```
```Nginx
server {
    listen 80 default_server;
    server_name smartbed;
    access_log /var/sites/smartbed/logs/access.log;
    error_log /var/sites/smartbed/logs/error.log;

    location /static/ {
        alias <SMARTBED_DIR>/app/static/;
    }

    location /media/ {
        alias <SMARTBED_DIR>/app/media/;
    }

    location / {
        uwsgi_pass unix:///run/uwsgi/smartbed.socket;
        include uwsgi_params;
    }

    error_page  404 /404.html;
    location = /40x.html {
        root   /usr/share/nginx/html;
    }

    error_page   500 502 503 504 /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

Add user to database
```sql
create database smartbed;
create role root with superuser, login;
```

## Credits

Frontend is based on CoreUI by mrholek
https://github.com/mrholek/CoreUI-Free-Bootstrap-Admin-Template