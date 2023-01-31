# On Termux: Use no docker:
Use master branch to delete for temux.
We do not use docker here, use nginx+django==2.2.0 instead.

# What's difference?
- Nginx conf. See ./termux_nginx_conf/nginx.conf, if you want to add password for nginx, you can re-run `htpasswd -c /xxxx/somewhere/passwd passwd` or use the passwd directly, and refresh the passwd path in nginx.conf .
- Uwsgi ini conf. Change for uwsgi start, and the way to start is in cmd below.
- Change path prefix. Use specific path prefix instead of `/src/` of docker.
- Cancel the validation code, for termux cannot install "pillow" package in python.

# Installation
- pkg install nginx, python3, pip3, uwsgi
- pip3 install django==2.2.0 django-cors-headers requests uwsgi

# cmd
```
# As dev_start.sh
# Please ensure the folder is existed: ./docker/log/
uwsgi --ini django1/uwsgi.ini
# uwsgi --reload uwsgi.pid
# uwsgi --stop uwsgi.pid
```

# Others
- add ssl version(termux nginx supports ssl, add pem/key location and run `nginx -s reload`)
- add kodbox conf for nginx at port 9011
unzip in index, and provide service at the whole port, use `php-fpm` to start(change /etc/php-fpm.d/www.conf file to modify `listen = /data/data/com.termux/files/usr/var/run/php-fpm.sock` to `listen = 127.0.0.1:9000`)
## ports:
django(8000) + nginx(9010)
php(9000) + nginx(9011)
