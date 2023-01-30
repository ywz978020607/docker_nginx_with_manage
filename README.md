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
