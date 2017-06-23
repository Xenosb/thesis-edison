# Thesis edison



## Requirements

On fedora
```
sudo dnf install python python-pip python-devel nginx postgresql gcc
sudo pip install uwsgi flask plim
```

On ubuntu/debian
```
sudo apt update
sudo apt install
sudo pip install uwsgi flask plim
```

## Setup

```/etc/systemd/system/smartbed.service```
```
[Unit]
Description=Smartbed uWSGI Service

[Service]
Environment="SMARTBED_DIR=/home/xeon/workspace_thesis/thesis-edison"
ExecStartPre=/usr/bin/bash -c 'mkdir -p /run/uwsgi; chown xeon:nginx /run/uwsgi'
ExecStart=/usr/bin/bash -c 'cd $SMARTBED_DIR/app; uwsgi --ini $SMARTBED_DIR/app/smartbed.ini;'

[Install]
WantedBy=multi-user.target
```

```
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

```/etc/nginx/sites-available/smartbed.conf```
```
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